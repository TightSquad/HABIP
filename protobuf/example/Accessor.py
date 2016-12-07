#!/usr/bin/env python

"""
tite: Protocol Buffer Tutorial
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Example code for the tutorial protocol buffer
"""

import tutorial_pb2 as tutorial

person = tutorial.Person()

person.id = 1
#person.name = "Mark Indovina"
#person.email = "maieee@rit.edu"

#phone = person.phone.add()
#phone.number = "585-777-7777"
#phone.type = tutorial.Person.MOBILE

pack = person.SerializeToString()

print len(pack)
print [c for c in pack]

newPerson = tutorial.Person()
newPerson.ParseFromString(pack)

#print newPerson.name, newPerson.email