## ncvlog-linter package


SystemVerilog linter using 'ncvlog' (Cadence Incisive) 

Only compiles the file being linted which keeps run time super speedy, and therefore the linter can work in-line during editing  (you might want https://atom.io/packages/autosave-onchange)

This downside to this approach, is that project-wide dependencies such as  'include filepaths , and module instantiations may give false positives / false negatives.

forked from :  https://github.com/KoenGoe/atom-vcs-linter)

### Dependencies :

1. 'ncvlog' available in your path
1. https://atom.io/packages/linter

### Under the hood

atom-ncvlog-linter runs the following command line each time the current file is saved (i.e. lint_test.v)

```
ncvlog -sv +incdir+. -logfile /tmp/logfile 
```


Each of the error messages are then parsed , and reformatted before being passed back to the linter package. I.e. :  

* Output from ncvlog 

```
ncvlog: 15.20-s060: (c) Copyright 1995-2018 Cadence Design Systems, Inc.
endmodule 
        |
ncvlog: *E,EXPLPA (lint_test.v,6|8): expecting a left parenthesis ('(') [12.1.2][7.1(IEEE)].
```

* input to Atom linter

```
lint_test.sv:6:Error:expecting a left parenthesis ('(') [12.1.2][7.1(IEEE)].
```

* linter message in Atom

![ncvlog-linter-screenshot](https://user-images.githubusercontent.com/68588485/91172343-ed2f2800-e6d3-11ea-8c56-accab977e416.png)

### ToDo

1. Add menu item so that additional command line options can be passed to ncvlog, such as additional files or include directories.

### Done 
1. Clean up INCA_libs
1. System level alert if ncvlog not found on command line
