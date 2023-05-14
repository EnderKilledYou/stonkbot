from flask import session, redirect, request, url_for, jsonify, Blueprint, abort
from forexconnect import ForexConnect

import common_samples
from sharp import sharp_api

tables = Blueprint('tables', __name__)


