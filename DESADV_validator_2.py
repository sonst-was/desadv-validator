from typing import IO, Iterator

file_in = 'G:\\Python\\DESADV-validator\\DESADV_no_line_break.txt'


def iter_file(file_: IO[str], separator: str = None, 
              chunk_size: int = 1024, include_separator: bool = False
              ) -> Iterator[str]:
    print('start2')
    excess = ''

    while True:
        # Read a chunk of the defined size from the file
        chunk = file_.read(chunk_size)
        if not chunk:
            if excess:
                yield excess
            print('nope')
            return
            
        chunk = excess + chunk
        *lines, excess = chunk.split(separator)
        print(lines)

        for line in lines:
            print(line)
            yield line + separator if include_separator else line
        chunk = excess



print('start')
print(*iter_file('G:\\Python\\DESADV-validator\\123.txt', '\''))
print('end')