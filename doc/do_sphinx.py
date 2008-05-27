import fileinput,os,sys

def oscmd(c):
    os.system(c)

# html manual.
oscmd('sphinx-build -d build/doctrees source build/html')

if sys.platform != 'win32':
    # LaTeX format.
    oscmd('sphinx-build -b latex -d build/doctrees source build/latex')

    # Produce pdf.
    os.chdir('build/latex')

    # Change chapter style to section style: allows chapters to start on 
    # the current page.  Works much better for the short chapters we have.
    # This must go in the class file rather than the preamble, so we modify 
    # manual.cls at runtime.
    chapter_cmds=r'''
% Local changes.
\renewcommand\chapter{
    \thispagestyle{plain}
    \global\@topnum\z@
    \@afterindentfalse
    \secdef\@chapter\@schapter
}
\def\@makechapterhead#1{
    \vspace*{10\p@}
    {\raggedright \reset@font \Huge \bfseries \thechapter \quad #1}
    \par\nobreak
    \hrulefill
    \par\nobreak
    \vspace*{10\p@}
}
\def\@makeschapterhead#1{
    \vspace*{10\p@}
    {\raggedright \reset@font \Huge \bfseries #1}
    \par\nobreak
    \hrulefill
    \par\nobreak
    \vspace*{10\p@}
}
'''

    unmodified=True
    for line in fileinput.FileInput('manual.cls',inplace=1):
        if 'Support for module synopsis' in line and unmodified:
            line=chapter_cmds+line
        elif 'makechapterhead' in line:
            # Already have altered manual.cls: don't need to again.
            unmodified=False
        print line,

    # Copying the makefile produced by sphinx...
    oscmd('pdflatex ipython.tex')
    oscmd('pdflatex ipython.tex')
    oscmd('pdflatex ipython.tex')
    oscmd('makeindex -s python.ist ipython.idx')
    oscmd('makeindex -s python.ist modipython.idx')
    oscmd('pdflatex ipython.tex')
    oscmd('pdflatex ipython.tex')
    oscmd('cp ipython.pdf ../html')
    os.chdir('../..')