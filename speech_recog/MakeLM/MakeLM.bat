:: �A���Ŏ��s����ƃp�X�������ăG���[�ɂȂ�̂�setlocal�ŗL���Ȕ͈͂����肷��
setlocal

:: Path�̐ݒ�
set PATH=%~p0;%PATH%
set PATH=%~p0;C:\Users\kuniyasu\Anaconda2;

:: �ꎞ�t�@�C���̒u���ꏊ���쐬
rd /s /q tmp
mkdir tmp

:: �e�L�X�g�𐮌`
python %~p0\preprocessText.py %1 > tmp/data.txt

::�P�ꔭ���p�x���v�Z
text2wfreq tmp/data.txt tmp/mklm.wfreq

::�P�ꃊ�X�g���쐬
wfreq2vocab -gt 0 tmp/mklm.wfreq tmp/mklm.vocab

::ID 3-gram���쐬
text2idngram -vocab tmp/mklm.vocab < tmp/data.txt > tmp/mklm.id3gram

::ID 2-gram���쐬
text2idngram -n 2 -vocab tmp/mklm.vocab < tmp/data.txt > tmp/mklm.id2gram

::3-gram���t���ɂ���
reverseidngram tmp/mklm.id3gram tmp/mklm.revid3gram

::3-gram���f���̍쐬
idngram2lm -idngram tmp/mklm.revid3gram -vocab tmp/mklm.vocab -arpa tmp/mklm.rev3gram.arpa

::2-gram���f���̍쐬
idngram2lm -n 2 -idngram tmp/mklm.id2gram -vocab tmp/mklm.vocab -arpa tmp/mklm.2gram.arpa

::1�̎����ɂ܂Ƃ߂�
mkbingram tmp/mklm.2gram.arpa tmp/mklm.rev3gram.arpa %2.bingram

::julius�p�̒P�ꎫ�����쐬
python %~p0\vocab2htkdict.py  tmp/mklm.vocab > %2.htkdic

endlocal