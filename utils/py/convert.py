#!/usr/bin/python
"""
utility to convert mp4 videos to 3gp.
my new basic nokia support 3gp.
Pre-requisites - ffmpeg

"""
import os
import sys

def main(basepath):
    """
    utility to convert mp4 videos to 3gp.
    my new basic nokia support 3gp.

    """
    srcpath = os.path.join(basepath,"from")
    tgtpath = os.path.join(basepath,"to")
    command = """ffmpeg -i %(src)s -s 352x288 -vcodec h263 -acodec aac -ac 1 -ar 8000 -r 25 -ab 32k -y -strict -2 %(tgt)s"""
    if not os.path.isdir(srcpath):
        os.mkdir(srcpath)
        print("I think you forgot to copy source files in from")
        return

    if not os.path.isdir(tgtpath):
        os.mkdir(tgtpath)

    for f in os.listdir(srcpath):
        if ".mp4" in f:
            #os.system("
            try:
                print("converting %s to %s" % (f, f.replace("mp4","3gp")))
                # TODO : supress the system command on sys out
                os.system(command % (
                    {'src': os.path.join(srcpath,f),
                    'tgt': os.path.join(tgtpath,f.replace("mp4","3gp"))}))

            except BaseException(e):
                print("Some unknown error ", e)

            finally:
                sys.stdout.buffer.flush()


if __name__ == "__main__":
    basepath = os.path.abspath("../../tests/utils/py/convert/")
    import pdb;pdb.set_trace()
    main(basepath)
