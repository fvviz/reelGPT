from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime, timedelta
from sys import stdout


VERSION = "1.1.0"


@dataclass
class SubtitleEntry:
    index: int
    start: datetime
    stop: datetime
    lines: list[str]

    @staticmethod
    def create(lines):
        index = int(lines.pop(0))
        tmp = lines.pop(0).split(" --> ")
        startstop = [datetime.strptime(x + "000", "%H:%M:%S,%f") for x in tmp]
        return SubtitleEntry(
            index=index, start=startstop[0], stop=startstop[1], lines=lines
        )

    def serialize(self):
        entry = []
        entry.append(f"{self.index}")
        entry.append(
            f"{self.start.strftime('%H:%M:%S,%f')[:-3]}"
            " --> "
            f"{self.stop.strftime('%H:%M:%S,%f')[:-3]}"
        )
        for line in self.lines:
            entry.append(line)
        return "\n".join(entry) + "\n\n"

    def adjust(self, seconds: float):
        td = timedelta(seconds=seconds)
        self.start += td
        self.stop += td


def get_subtitles(infile):
    """
    Generator which returns subtitles from a given already opened input file.

    Yields a list which is basically all lines between empty lines in the
    subtitles file.

    :param infile: The opened file-handle (or file-like object)
    :return: Yields [line1, line2, ...] of each subtitle block
    """
    line = "start"
    try:
        while line:
            line = infile.readline()
            if not line.strip():
                continue
            st = [line.strip(), infile.readline().strip()]
            line = infile.readline()
            while line.strip():
                st.append(line.strip())
                line = infile.readline()
            yield SubtitleEntry.create(st)
    except UnicodeDecodeError as e:
        print("UNICODE ERROR on or after line: ", line)
        raise e


def adjust_subtitles(outfile, offset):
    """
    Opens config.srt_file as subtitle file, then iterates thorugh all subtitles
    and adjusts the start and stop times using the adjust_subtitle function.
    :param outfile: The output file handle (or any file-like object)
    :return: None
    """
    td = timedelta(seconds=offset)
    # see http://stackoverflow.com/a/2459793/902327
    with open(outfile, "r", encoding="utf-8-sig") as infile:
        # we manually count indexes, cause we don't know how many we skip ...
        index = 1
        for se in get_subtitles(infile):
            se.adjust(offset)
            if se.start.hour > 20:
                continue
            se.index = index
            index += 1
            outfile.write(se.serialize())


def start(file, offset):
    """
    The starting point of everything.
    :return: None
    """

    adjust_subtitles(file, offset)
    
