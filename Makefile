simple:
	./Test.py < data/simple.in | diff data/simple.out -
1k:
	./Test.py < data/1k.in | diff data/1k.out -
10k:
	./Test.py < data/10k.in | diff data/10k.out -
100k:
	./Test.py < data/100k.in | diff data/100k.out -
