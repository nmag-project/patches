# NMAG Mods

This is a patch for the NMAG nanomagnetic simulation suite which allows it to compile on modern Ubuntu systems. It currently supports Ubuntu 20.04. Going forward, releases will be tagged with the version of Ubuntu that they support.

## NMAG Resources

- [Official Repository](https://github.com/fangohr/nmag-src)
- [Official Website](https://fangohr.github.io/nmag.github.io/)
- [Documentation](https://nmag.readthedocs.io/en/latest/)

## Building

To apply the patches and build NMAG:

```
./build.sh
```

## Patches

In case you're curious, the build script makes the following changes:

- Removes dependencies from the Makefile that can no longer be compiled
- Installs newer versions of those dependencies which could no longer be compiled
- Replaces the old shell.py interface with one that uses updated syntax
- Updates deprecated pytables syntax 

