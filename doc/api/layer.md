## Layer

A layer is a group of elements. All elements have to be associated with a layer.


### GET /api/layer/?\<params>

This method gets layers from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - layer_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - is_published (optional): it is a boolean that indicates if a layer is published or not (e.g. 'TRUE' or 'FALSE');
    - f_table_name (optional): the name of the table that is a text (e.g. '_1005_layer_1003').
- Examples:
     - Get all layers: http://localhost:8888/api/layer/
     - Get one layer by id: http://localhost:8888/api/layer/?layer_id=1001
     - Get layers by is_published: http://localhost:8888/api/layer/?is_published=TRUE
     - Get one layer by f_table_name: http://localhost:8888/api/layer/?f_table_name=layer_1003
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'user_id_published_by': 1003, 'is_published': True, 'description': '',
                               'name': 'Robberies between 1880 to 1900',
                               'reference': [{'reference_id': 1005, 'bibtex': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}],
                               'layer_id': 1002, 'f_table_name': 'layer_1002', 'source_description': '',
                               'created_at': '2017-03-05 00:00:00'},
                'type': 'Layer'
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### PUT /api/layer/create/?\<params>

This method creates a new layer described in a JSON.
- Parameters:
    - is_to_create_feature_table (optional): it is a boolean that indicates if a feature table will be created together the layer or not (e.g. 'TRUE' or 'FALSE'; default is 'TRUE');
- Examples:
    - Create a layer with feature table: ```PUT http://localhost:8888/api/layer/create```
    - Create a layer without feature table: ```PUT http://localhost:8888/api/layer/create/?is_to_create_feature_table=FALSE```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'Layer',
        'properties': {'layer_id': -1, 'f_table_name': 'new_layer', 'name': 'Addresses in 1930',
                       'description': '', 'source_description': '',
                       'reference': [], 'theme': [{'theme_id': 1041}]},
        'feature_table': {
            'properties': {'name': 'text', 'start_date': 'text', 'end_date': 'text'},
            'geometry': {"type": "MultiPoint"}
        }
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'layer_id': 7}
    ```
- Error codes:
    - 400 (Bad Request): Table name already exists.
    - 400 (Bad Request): The parameter reference needs to be a list.
    - 400 (Bad Request): It is necessary a reference parameter.
    - 403 (Forbidden): It is necessary an Authorization header valid.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:
    - The parameter "is_to_create_feature_table" is usually used when is not necessary to create a feature table for the layer (e.g. when import a ShapeFile, it will be the feature table).
    - The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- - PUT /api/layer/update -->


### DELETE /api/layer/#id

This method deletes one layer by id = #id.
- Parameters:
    - #id (mandatory): the id of the resource that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/layer/7```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary an Authorization header valid.
    - 403 (Forbidden): The owner of the layer is the unique who can delete the layer.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:


## User_Layer

Users who is part of a layer.


### GET /api/user_layer/?\<params>

This method gets users in layers from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - layer_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - user_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - is_the_creator (optional): it is a boolean that indicates if a user is or not the creator of the layer (e.g. 'TRUE' or 'FALSE').
- Examples:
     - Get all users in layers: http://localhost:8888/api/user_layer/
     - Get users that belongs to a layer by id: http://localhost:8888/api/user_layer/?layer_id=1001
     - Get layers of a user by id: http://localhost:8888/api/user_layer/?user_id=1001
     - Get layers of a user who he/she is the creator by id: http://localhost:8888/api/user_layer/?user_id=1001&is_the_creator=TRUE
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the selected resources. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'is_the_creator': True, 'user_id': 1005, 'layer_id': 1003,
                               'created_at': '2017-04-10 00:00:00'},
                'type': 'Layer'
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### PUT /api/user_layer/create

This method adds a user in a layer described in JSON.
- Parameters:
- Examples:
    - Add a user in a layer: ```PUT http://localhost:8888/api/user_layer/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'is_the_creator': False, 'user_id': 1004, 'layer_id': 1003},
        'type': 'UserLayer'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Table name already exists.
    - 400 (Bad Request): The parameter source needs to be a list.
    - 403 (Forbidden): It is necessary an Authorization header valid.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:


<!-- - PUT /api/layer/update -->


### DELETE /api/user_layer/?\<params>

This method remove a user from a layer.
- Parameters:
    - layer_id (mandatory): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - user_id (mandatory): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...);
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/user_layer/?layer_id=1001&user_id=1004```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary an Authorization header valid.
    - 403 (Forbidden): The owner of the layer is the unique who can delete the layer.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes: