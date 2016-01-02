#!/usr/bin/env python

class AutoVivification(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value