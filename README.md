# Applying Named Config Templates

Did you know that you can apply those XML templates to transactions
without using a service? You can, but only from code. This small
package defines an action that applies your named templates, that way
you will have access to the functionality from the CLI and all enabled
northbound api:s.

## Requirements and How to Build

The package contains YANG and Python code, so you will need NSO and
Python. There are no other dependencies.

To build:

    cd src && make


## How to Use

Load the apply-config-template package into your NSO installation. You
will also need another package that has templates installed. Here is a
sample from the test directory:

```
admin@ncs> show packages package | select package-version | select templates 
                       PACKAGE                       
NAME                   VERSION  TEMPLATES            
-----------------------------------------------------
apply-config-template  1.0      -                    
frobnicator            1.0      [ frobnicator-foo ]  

[ok]
```

The package "frobnicator" has one template which is called
"frobnicator-foo", let's apply it:

```
admin@ncs> configure
Entering configuration mode private
[ok]

[edit]
admin@ncs% request template apply-config-template name frobnicator-foo variable { name DEVICE value frob0 }
[ok]

[edit]
admin@ncs% request template apply-config-template name frobnicator-foo variable { name DEVICE value frob1 }
[ok]

[edit]
admin@ncs% commit 
Commit complete.
[ok]
```



## Tests

The [test directory](./test/) contains a couple of
[LuX](https://github.com/hawk/lux) scripts which invoke the action
from different northbound API:s (CLI, NETCONF, REST, RESTCONF, and
Python).

To test, simply run `make test` in the test directory.
