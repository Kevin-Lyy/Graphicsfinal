test: simple_anim.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py simple_anim.mdl

face: face.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py face.mdl

diamond: diamond.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py diamond.mdl

cube: cube.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py cube.mdl

clean:
	rm *pyc *out parsetab.py
	rm ./anim/*.png

clear:
	rm *pyc *out parsetab.py *ppm
