lamp: lamp.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py lamp.mdl

face: face.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py face.mdl

simple: simple_anim.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py simple_anim.mdl

shuttle: shuttle.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py shuttle.mdl

cube: cube.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py cube.mdl

violin: violin.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py violin.mdl

al: al.mdl lex.py main.py matrix.py mdl.py display.py draw.py gmath.py yacc.py
	python main.py al.mdl


clean:
	rm *pyc *out parsetab.py
	rm ./anim/*.png

clear:
	rm *pyc *out parsetab.py *ppm
