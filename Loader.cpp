// simple loader 
// 22 Jan 2020 HS kim

#include <stdio.h>
#include <Windows.h>
#include <Shlwapi.h>

int numArgs = 0;
DWORD readOffset = 0;
DWORD executeOffset = 0;

BOOL toBeExecuted = false;

void printUsage()
{
	wprintf(L"+============================================================================+\n");
	wprintf(L"| Usage:                                                                     |\n");
	wprintf(L"+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -+\n");
	wprintf(L"| Loader.exe [target_file] ( -r[read_offset_hex] ) ( -x[execute_offset_hex] )|\n");
	wprintf(L"| Loader.exe -h for more examples!                                           |\n");
	wprintf(L"+============================================================================+\n");
}

void printExamples()
{
	wprintf(L"+============================================================================\n");
	wprintf(L"| More Examples:\n");
	wprintf(L"+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n");
	wprintf(L"| Loader.exe c:\\temp\\test.bin            (read test.bin from offset 0x00  and do not execute)\n");
	wprintf(L"| Loader.exe c:\\temp\\test.bin -r100      (read test.bin from offset 0x100 and do not execute)\n");
	wprintf(L"| Loader.exe c:\\temp\\test.bin -r10 -x100 (read test.bin from offset 0x10  and execute from 0x100)\n");
	wprintf(L"| Loader.exe c:\\temp\\test.bin -x6f       (read test.bin from offset 0x00  and execute from 0x6f)\n");
	wprintf(L"| Loader.exe c:\\temp\\test.bin -r100 -x   (read test.bin from offset 0x100 and execute from 0x00)\n");
	wprintf(L"| Loader.exe c:\\temp\\test.bin -x         (read test.bin from offset 0x00  and execute from 0x00)\n");
	wprintf(L"| * Note that -x0 and -x is the same (Executing from offset 0x00)\n");
	wprintf(L"+============================================================================\n");
}

int checkNibble(BYTE b)
{
	if (0x30 <= b && b <= 0x39)
	{
		return b - 0x30;
	}

	else if (0x41 <= b && b <= 0x4f)
	{
		return b - 0x37;		// if A-F -> return 0xA - 0xF
	}

	else if (0x61 <= b && b <= 0x6f)
	{
		return b - 0x57;		// if A-F -> return 0xA - 0xF
	}

	else
	{
		return -1;
	}
}

DWORD parseOffset(LPWSTR str)
{
	int sLen = wcsnlen(str, 10);	// 8 for DWORD and 2 for switches (-e)
	DWORD nibble = 0;
	DWORD result = 0;

	for (int i = 0; i < sLen - 2; i++)
	{
		nibble = checkNibble( (BYTE) str[sLen - 1 - i]);
		if (nibble == -1)
		{
			printUsage();
			return -1;
		}
		result += nibble << (4 * i);
	}

	return result;
}

BOOL parseCommandLine(LPWSTR* cmdlines)
{
	if (numArgs == 2)
	{
		if (cmdlines[1][0] == '-' && cmdlines[1][1] == 'h')
		{
			if (wcsnlen(cmdlines[1], 10) == 2)
			{
				printExamples();
			}
			return false;
		}
		else
		{
			if (!PathFileExistsW(cmdlines[1]))
			{
				wprintf(L"Invalid Path\n");
				return false;
			}
		}
	}

	if (numArgs == 3)
	{
		if (cmdlines[2][0] == '-')
		{
			if (cmdlines[2][1] == 'r')
			{
				readOffset = parseOffset(cmdlines[2]);
			}

			else if (cmdlines[2][1] == 'x')
			{
				executeOffset = parseOffset(cmdlines[2]);
				toBeExecuted = true;
			}

			else if (cmdlines[2][1] == 'h')
			{
				if (wcsnlen(cmdlines[2], 10) == 2)
				{
					printExamples();
				}
				return false;
			}

			else
			{
				wprintf(L"[ERROR] Not a valid switch (r or x)\n");
				return false;
			}
		}
		else
		{
			wprintf(L"[ERROR] Not a valid switch (starts with -)\n");
			return false;
		}
	}

	if (numArgs == 4)
	{
		if (cmdlines[2][0] == '-')
		{
			if (cmdlines[2][1] == 'r')
			{
				readOffset = parseOffset(cmdlines[2]);
			}
			else if (cmdlines[2][1] == 'x')
			{
				executeOffset = parseOffset(cmdlines[2]);
				toBeExecuted = true;
			}

			else if (cmdlines[2][1] == 'h' && wcsnlen(cmdlines[2], 10) == 2)
			{
				if (wcsnlen(cmdlines[2], 10) == 2)
				{
					printExamples();
				}
				return false;
			}

			else
			{
				wprintf(L"[ERROR] Not a valid switch (r or x)\n");
				return false;
			}
		}

		if (cmdlines[3][0] == '-')
		{
			if (cmdlines[3][1] == 'r')
			{
				readOffset = parseOffset(cmdlines[3]);
			}
			else if (cmdlines[3][1] == 'x')
			{
				executeOffset = parseOffset(cmdlines[3]);
				toBeExecuted = true;
			}

			else if (cmdlines[3][1] == 'h' && wcsnlen(cmdlines[3], 10) == 2)
			{
				if (wcsnlen(cmdlines[3], 10) == 2)
				{
					printExamples();
				}
				return false;
			}

			else
			{
				wprintf(L"[ERROR] Not a valid switch (r or x)\n");
				return false;
			}
		}

		else
		{
			wprintf(L"[ERROR] Not a valid switch (starts with -)\n");
			return false;
		}
	}

	return true;
}

int main()
{
	wprintf(L"+============================================================================+\n");
	wprintf(L"| SHELLOADEX                                                                 |\n");
	wprintf(L"+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -+\n");
	wprintf(L"| a simple loader that can load a shellcode and execute it (optional)        |\n");
	wprintf(L"| by hazelash - Jan 2020                                                     |\n");

	printUsage();

	DWORD dwReadSize = 0;
	DWORD dwExit = 0;

	HANDLE hFile = NULL;

	LPVOID lpBuffer = NULL;
	LPVOID lpBaseAddress = NULL;

	LPDWORD lpActualRead = 0;
	LPOVERLAPPED lpOverlapped = NULL;

	// x64 and x86 builds
	LPWSTR* cmdlines = CommandLineToArgvW(GetCommandLineW(), &numArgs);
	if (cmdlines == NULL)
	{
		wprintf(L"Error with GetCommandLine\n");

		dwExit = -1;
		goto __FREE_NONE;
	}

	// falls between 2, 3, 4
	if (numArgs < 2 || 4 < numArgs)
	{
		wprintf(L"[ERROR] Wrong number of arguments\n");

		dwExit = -1;
		goto __FREE_NONE;
	}

	if (!parseCommandLine(cmdlines))
	{
		wprintf(L"parseCommandLine Fail\n");
		dwExit = -1;
		goto __FREE_NONE;
	}

	hFile = CreateFileW(cmdlines[1], GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
	if (hFile == NULL)
	{
		wprintf(L"Error with CreateFileW\n");

		dwExit = -1;
		goto __FREE_NONE;
	}

	dwReadSize = GetFileSize(hFile, NULL);
	if (dwReadSize == INVALID_FILE_SIZE)
	{
		wprintf(L"Error with GetFileSize\n");

		dwExit = -1;
		goto __FREE_NONE;
	}

	lpBuffer = (BYTE*)malloc(dwReadSize);
	if (!lpBuffer)
	{
		wprintf(L"Error with malloc\n");

		dwExit = -1;
		goto __FREE_NONE;
	}

	if (!ReadFile(hFile, lpBuffer, dwReadSize, lpActualRead, lpOverlapped))
	{
		wprintf(L"Error with ReadFile\n");

		dwExit = -1;
		goto __FREE_ONE;
	}

	if (readOffset > dwReadSize)
	{
		wprintf(L"Invalid offset for read (Size of file: %x, requested: %x)\n", dwReadSize, readOffset);

		dwExit = -1;
		goto __FREE_ONE;
	}

	lpBaseAddress = VirtualAlloc(NULL, dwReadSize, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
	if (!lpBaseAddress)
	{
		wprintf(L"Error with VirtualAlloc\n");

		dwExit = -1;
		goto __FREE_ONE;
	}

	memcpy(lpBaseAddress, lpBuffer, dwReadSize);

	if (executeOffset > dwReadSize)
	{
		wprintf(L"Invalid offset for execution (Size of shellcode: %x, requested: %x)\n", dwReadSize, executeOffset);

		dwExit = -1;
		goto __FREE_ALL;
	}

	if (toBeExecuted)
	{
		wprintf(L"Now the shellcode is executed... (Ctrl+C to stop)\n");
		void(*funcAddr)();
		funcAddr = reinterpret_cast<void(*)()>(LPVOID((int)lpBaseAddress + executeOffset));
		funcAddr();
	}

	else
	{
		wprintf(L"Operation complete - you chose to not execute\n");
		wprintf(L"Maybe you want to load this with a debugger?\n");
	}

__FREE_ALL:
	VirtualFree(lpBaseAddress, NULL, MEM_RELEASE);

__FREE_ONE:
	free(lpBuffer);

__FREE_NONE:
	return dwExit;

}
