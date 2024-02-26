# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 21:51:19 2020

@author: win10
"""
from pydantic import BaseModel
from typing import Any
# 2. Class which describes Bank Notes measurements
class Applicant(BaseModel):
    id : int
    position: Any
    skills: Any
    education: Any
    location: Any