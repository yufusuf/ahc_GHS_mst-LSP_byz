# Distributed Algorithms on AHCv2

This is a template project for implementing distributed algorithms on AHCv2. By cloning and using this repository, you agree to GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007. 

## Install AHCv2

```pip3 install adhoccomputing```

or alternatively,

```
git clone https://github.com/cengwins/ahc.git
cd ahc
pip3 install .
```

or alternatively, you can checkout this project and run `make ahc`.

## Before Starting Implementation

There are some issues you have to address before starting implementation, please:


- rename the keyword `distalgname` in any foldername (/distalgname and /docs/disalgname), in any filenames (docs/distalgname/distalgname.rst) and in any fields in any file (all instances in index.rst) to a **meaningfull abbreviation** of your distributed algorithm. Note that doc/substitutions.rst defines a keywork |DistAlgName| that has to be changed as well.
- user restructured text for documentation. There is a conf.py and the associated Makefile in the project's root directory. Running``make`` in the project's root directory will provide you a guide on how to build the html, pdf, epub, etc. documentation. 
- do not edit anything in `build`, `_static`, `_templates` directories.  
- in conf.py edit `project, copyright, author, release` fields.
- list your modules in code.rst under docs/distalgname






