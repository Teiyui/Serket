# encoding: shift_jis
import codecs
import sys

def ReplaceInvalidTransition( str ):
    for c in ("��" , "��" , "��", "��", "��", "��", "��", "��"):
        str = str.replace( " " + c , c )

    return str

def main():
    for line in codecs.open( sys.argv[1] ).readlines():
        line = line.replace("\r","").replace("\n" , "")

        if len(line)==0:
            continue

        if line[:3] != "<s>":
            line = "<s> " + line
        if line[-4:] != "</s>":
            line = line + " </s>"

        # ��؂蕶����space�œ���
        line = line.replace("|" , " " )
        line = line.replace("," , " " )
        line = line.replace("\t" , " " )

        while "  " in line:
            line = line.replace("  " , " ")

        line = ReplaceInvalidTransition(line)

        print( line )

if __name__ == '__main__':
    main()
