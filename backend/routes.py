from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all pictures."""
    if data:
        return jsonify(data), 200
    return {"message": "No pictures found"}, 404


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by its ID."""
    # Buscar la imagen por ID
    picture = next((item for item in data if item["id"] == id), None)
    
    if picture:
        return jsonify(picture), 200  # Imagen encontrada, retornar con 200 OK
    return {"message": "Picture not found"}, 404  # Imagen no encontrada



######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    """Create a new picture entry."""
    if not request.is_json:
        return {"message": "Request body must be JSON"}, 400

    picture = request.get_json()

     # Verificar si la imagen ya existe por ID
    existing_picture = next((item for item in data if item["id"] == picture["id"]), None)
    if existing_picture:
        return {
            "Message": f"picture with id {picture['id']} already present"
        }, 302

    # Agregar nueva imagen a la lista
    data.append(picture)
    return jsonify(picture), 201





######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """Update an existing picture."""
    if not request.is_json:
        return {"message": "Request body must be JSON"}, 400

    updated_picture = request.get_json()

    # Buscar la imagen existente por ID
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "picture not found"}, 404

    # Actualizar los campos de la imagen
    picture.update(updated_picture)
    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """Delete a picture by its ID."""
    # Find the picture by ID
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        return {"message": "picture not found"}, 404

    # Remove the picture from the list
    data.remove(picture)
    return "", 204  # No content
