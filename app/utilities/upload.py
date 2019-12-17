# from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
# from flask import request, jsonify, abort, make_response, current_app as app
# from api.trainers.controllers import user_valid
# from api.trainers.models import Trainer
# from api.pools.models import Pool
# from api.auth.models import User
# from api.database.db import db
# from api.images.models import Images
# from app.utilities.flask_imgur import Imgur

# import os


# images = ('jpg', 'jpeg', 'png', 'gif')
# # base_url = 'https://swimsafeapp.herokuapp.com/uploads'
# base_url = 'http://127.0.0.1:5000/api/v1/uploads'


# # Initialise uploadset for pictures only
# photos = UploadSet('photos', extensions=images)


# def check_if_image_is_already_uploaded(fetched_image_url, upload_image_url):
#     """
#     Check if image exists
#     """
#     if str(fetched_image_url) == str(upload_image_url):
#         abort(make_response(jsonify({'message': 'File already exists',
#                                      'status': 400})))


# def upload_file(current_user, **kwargs):
#     imgur = Imgur(app)
#     user_valid.check_user_is_loggedin(current_user)
#     if request.method == 'POST' and 'file' in request.files:
#         # Check if the file has a valid extension
#         file_name = request.files['file']
#         split_filename_and_extension = os.path.splitext(file_name.filename)
#         file_extension = split_filename_and_extension[1]
#         if not file_extension[1:] in images:
#             return jsonify({'message': 'Wrong file type. only jpg,jpeg,png and gif images are allowed',
#                             'status': 400})
#         table_name = kwargs.get('table')
#         pool_id = kwargs.get('pool_id')
#         trainer_id = kwargs.get('trainer_id')
#         user_id = kwargs.get('user_id')
#         image_data = imgur.send_image(file_name)
#         file_url = image_data["data"]["link"]
#         if table_name == 'pools':
#             pool_fetch_data = Pool.query.filter_by(pool_id=pool_id).first()
#             if not pool_fetch_data:
#                 return jsonify({'message': 'Swimming pool not found',
#                                 'status': 404})
#             check_if_image_is_already_uploaded(
#                 pool_fetch_data.pool_thumbnail, file_url)
#             setattr(pool_fetch_data, 'pool_thumbnail', file_url)
#             db.session.commit()
#         elif table_name == 'trainer':
#             trainer_fetch_data = Trainer.query.filter_by(
#                 trainer_id=trainer_id).first()
#             if not trainer_fetch_data:
#                 return jsonify({'message': 'Trainer not found',
#                                 'status': 404})
#             check_if_image_is_already_uploaded(
#                 trainer_fetch_data.trainer_img, file_url)
#             setattr(trainer_fetch_data, 'trainer_img', file_url)
#             db.session.commit()
#         elif table_name == 'user':
#             user_fetch_data = User.query.filter_by(user_id=user_id).first()
#             if not user_fetch_data:
#                 return jsonify({'message': 'User information was not found',
#                                 'status': 404})
#             check_if_image_is_already_uploaded(
#                 user_fetch_data.user_pic, file_url)
#             setattr(user_fetch_data, 'user_pic', file_url)
#             db.session.commit()
#         else:
#             fetch_images = Images.query.all()
#             if fetch_images:
#                 for image_info in fetch_images:
#                     check_if_image_is_already_uploaded(
#                         image_info.image_url, file_url)
#             image = Images(image_name=file_name.filename, image_url=file_url,
#                            pool_id=pool_id)
#             db.session.add(image)
#             db.session.commit()
#         return jsonify({'message': 'Image uploaded successfully',
#                         'status': 201})
#     return jsonify({'message': 'Upload failed', 'status': 400})
