# test: examples/simple_anim.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
# 	python main.py examples/simple_anim.mdl
#
# mesh: face.mdl diamond.obj lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
# 	python main.py face.mdl
#
# shade: face.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
# 	python main.py face.mdl
#
# face: face.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
# 	python main.py face.mdl
#
# move: move.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
# 	python main.py move.mdl
#
# clean:
# 	rm *pyc *out parsetab.py
# 	rm anim/*
#
# clear:
# 	rm *pyc *out parsetab.py *ppm

test: face.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py simple_anim.mdl

clean:
	rm *pyc *out parsetab.py
	rm ./anim/*.png

clear:
	rm *pyc *out parsetab.py *ppm
