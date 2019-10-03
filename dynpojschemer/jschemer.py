import json
import random

from dynpoinput import Inputer


class JSchemer:
    """
    Generate json automated or interactive json sample.

    OBJECTIVE:
    -From jSON Schema used in OpenAPI documentation, generate a json sample.
    -Users can provide a Random Pool of values to be used on the sample
     generation
    -Users can opt for interactive sample generation where each object requests
     information from user, it only accepts valid data to generate json object.
    
    BUT HOW?
    -It generates a map of the json keys in the schema, which is a var named:
    iter_cursor_collection.
    -It generates a map of the json keys that should be in the sample, which is
    a var named: result_cursor_collection.
    -It uses the schema description to decite what type of data is necessary in
    the sample.
    -It uses the result_cursor_collection to allocate that in the correct spot.
    -If interactive sample is select, it then uses input() to get that and
    validates it according to the schema definition.
    
    REQUIREMENTS:
    -This was created to iterate over jSON Schema used in OpenAPI definitions,
    mre specifically, Rubrik's OpenApi definition.
    -If using this librabry in another definition be aware it might be missing
    bits and pieces.
    """
    JSCHEMA_PROTECTED = {
        'title': '',
        'multipleOf': '',
        'maximum': '',
        'exclusiveMaximum': '',
        'minimum': '',
        'exclusiveMinimum': '',
        'maxLength': '',
        'minLength': '',
        'pattern': '',
        'maxItems': '',
        'minItems': '',
        'uniqueItems': '',
        'maxProperties': '',
        'minProperties': '',
        'required': '',
        'enum': '',
        'type': '',
        'allOf': '',
        'oneOf': '',
        'anyOf': '',
        'not': '',
        'items': '',
        'properties': '',
        'additionalProperties': '',
        'description': '',
        'format': '',
        'default': '',
        'schema': '',
        'in': '',
        'x-secret': ''
    }

    RANDOM_POOL = {
        'string': ['A_word_please', 'More than words'],
        'boolean': [False, True],
        'integer': [7, 1, 12, 17, 9],
        'number': [1.00, 62.00, 29.00],
        'object': [{}],
        'array': [{}]
    }

    unchangeable_types = {
        'object': '',
        'array': '',
        'empty': ''
    }

    jython_type = {
        'string': str,
        'number': float,
        'integer': int,
        'boolean': bool
    }

    # Declare variables used in all iterations.
    iter_cursor = []
    iter_cursor_collection = []

    result_cursor = []
    result_cursor_collection = []
    result_cursor_flag = ''

    result_json = {}
    result_builder = {}

    def __init__(self, json_data):
        """Initialize json schemer class."""
        self.json_data = json_data
        self.inputer = Inputer()
        self.required_keys = []

    def sample(self, interactive=False):
        """Generate json sample from instantiated schema."""
        self.interactive = interactive
        self.schema_name = list(self.json_data['schema'].keys())[0]

        self._print_interactive(' - Creating a [%s]\n' % self.schema_name)

        self._iterate_json(self.json_data)
        return self.result_builder

    def _print_interactive(self, string):
        if self.interactive:
            print(string)

    def _iterate_json(self, json_data):
        """Iterate json data per data type."""
        if isinstance(json_data, dict):
            json_data = self._iterate_dict(json_data)
        if isinstance(json_data, list):
            json_data = self._iterate_list(json_data)
        else:
            json_data = self._iterate_other(json_data)

        return json_data

    def _iterate_dict(self, json_data):
        """Iterate dictionary."""
        # Declare new dict value to be returned.
        new_dict = {}

        # Iterate dict json data.
        for k, v in json_data.items():

            # Update cursor
            self.iter_cursor.append(k)
            inx = len(self.iter_cursor) - 1

            # Include current cursor in the collection
            self._update_cursor_collection()

            # Verify if current level has required child.
            self._verify_child_elements(k, v, json_data)

            # Verify if key is schema language or content.
            current_cursor_inx, cursor_flag, array_flag = \
                self._verify_key_identity(k, v, json_data)

            # Iterate any possible child.
            new_dict[k] = self._iterate_json(v)

            # Treat final cursor
            if cursor_flag == k:
                self._accumulate_cursor(current_cursor_inx,
                                        new_array=array_flag)

            # Update cursor
            self.iter_cursor.pop(inx)

        return new_dict

    def _iterate_list(self, json_data):
        """Iterate list."""
        # Declare new list value to be returned.
        new_dict = []

        # Iterate list json data.
        for element in enumerate(json_data):

            # Update cursor
            self.iter_cursor.append(element[0])
            inx = len(self.iter_cursor) - 1

            # Iterate any possible child.
            new_dict.append(self._iterate_json(element[1]))

            # Update cursor
            self.iter_cursor.pop(inx)

            # Treat final cursor
            if self.result_cursor_flag == element[0]:
                # Include current cursor in the collection
                self._update_cursor_collection()
                self.result_cursor.remove(self.result_cursor_flag)

        return new_dict

    def _iterate_other(self, json_data):
        """Iterate any other type of data."""
        return json_data

    def _update_cursor_collection(self):
        """Update the cursor collection with the key being iterated."""
        line = ''
        for item in self.iter_cursor:
            line = line + '[%s]' % str(item)
        self.iter_cursor_collection.append(line)

    def _verify_child_elements(self, key, value, json_data):
        """Get properties of child elements."""
        if key == 'properties':
            self._get_required_keys(key, value, json_data)

        return json_data

    def _get_required_keys(self, key, value, json_data):
        """Get required keys for a specific object."""
        if 'required' in json_data.keys():
            self.required_keys = json_data['required']
            # Create required_key_cursor, to check upon when iterating the key.
            #print(self.result_cursor)
            #print(json_data['required'])


    def _verify_required(self, key, value, json_data):
        """Remove key from required keys once it was iterated."""
        if key in self.required_keys:
            self.required_keys.remove(key)
            return True
        else:
            return False

    def _verify_key_identity(self, key, value, json_data):
        """Identify what type of key is this in the grater schema."""
        array_flag = False
        cursor_inx = 0
        cursor_flag = ''
        # If key is not a protected element.
        if key not in self.JSCHEMA_PROTECTED:

            # Get the type description of that key.
            key_type = self._get_key_type(key, value, json_data)

            # If the key type is allows to change the value.
            if key_type not in self.unchangeable_types:

                # Check if it is a required key.
                required = self._verify_required(key, value, json_data)

                # Get the new value with the appropriated conditions.
                self._get_new_value(key,
                                    value,
                                    json_data,
                                    key_type,
                                    required=required)

                # Deal with cursor flag.
                self.result_cursor_flag = key
                self.result_cursor.append(key)
                cursor_inx = len(self.result_cursor) - 1
                cursor_flag = self.result_cursor_flag

            else:
                # If key type is not empty than it means the key should
                # be part of the final json result.
                if key_type == 'array':
                    array_flag = True
                    self._introduce_object(key_type, key)

                    # REsult assignament
                    if not self.result_cursor:
                        self.result_builder[key] = [{}]
                        self.result_json = self.result_builder[key][0]
                    else:
                        result = self._add_object_oriented(key, [{}])
                        self.result_json = result[key][0]

                        # Deal with cursor flag.
                    self.result_cursor_flag = key
                    self.result_cursor.append(self.result_cursor_flag)
                    self.result_cursor.append(0)
                    cursor_inx = len(self.result_cursor) - 1
                    cursor_flag = self.result_cursor_flag

                elif key_type == 'empty':
                    if not key[0].isupper():
                        self._introduce_object(key_type, key)
                        # Result assignament
                        if not self.result_cursor:
                            self.result_builder[key] = {}
                            self.result_json = self.result_builder[key]
                        else:
                            result = self._add_object_oriented(key, {})
                            self.result_json = result[key]

                        # Deal with cursor flag.
                        self.result_cursor_flag = key
                        self.result_cursor.append(key)
                        cursor_inx = len(self.result_cursor) - 1
                        cursor_flag = self.result_cursor_flag

        return cursor_inx, cursor_flag, array_flag

    def _get_key_type(self, key, value, json_data):
        """Get the schema type definitions for this key."""
        try:
            # If there is a type definition load it.
            if 'type' in value.keys():
                key_type = value['type']
            # If not load as empty.
            else:
                key_type = 'empty'
        except AttributeError as error:
            msg = str('Got error while iterating key [%s] and value [%s].\n'
                      'Error: %s' % (key, str(value), str(error)))
            raise Exception(msg)

        return key_type

    def _get_new_value(self, key, value, json_data, k_type, required=None):
        """Get new value for the sample."""
        description = self._get_key_description(key, value, json_data)
        if self.interactive:
            #
            if description != 'empty':
                a_description = ', Description: %s' % description
            else:
                a_description = ''

            msg = 'Field: %s%s\nPlease provide [%s]: ' % (key, a_description, key)
            user_input = self.inputer.get_input(msg=msg,
                                               required=required,
                                               data_type=k_type)
            new_input = user_input['data']
            skipped = user_input['skiped']
            #new_input = self._get_user_value(key, k_type, description, required)
        else:
            skipped = False
            new_input = self._get_random_value(k_type)

        if not skipped:
            if isinstance(self.result_json, dict):
                if not self.result_cursor:
                    self.result_builder[key] = new_input
                else:
                    self._add_object_oriented(key, new_input)

            elif isinstance(self.result_json, list):
                self.result_json.append(new_input)

    def _get_key_description(self, key, value, json_data):
        """Get key description to use in the interactive sample."""
        # If there is a type definition load it.
        if 'description' in value.keys():
            description = value['description']

        # If not load as empty.
        else:
            description = 'empty'

        return description

    def _verify_skip_request(self, new_input, required):
        """Verify if skip request is acceptable."""
        accepted = False
        if new_input == 'S' or new_input == 's':
            if not required:
                accepted = True
            else:
                print('ERROR: This key is required and canno\'t be skipped!')
                accepted = False

        return accepted

    def _get_user_value(self, key, k_type, description, required):
        """Get new value from user, interactively."""

        accepted = False
        while accepted is False:
            new_input = input('ACTION: Please provide a [%s] value for key'
                              ' [%s].\nDESCRIPTION: %s\n[s/S to skip this '
                              'key]: ' % (k_type, key, description))

            # Fix skip requesssttto-da
            accepted = self._verify_skip_request(new_input, required)

            if not accepted:
                try:
                    new_input = self.jython_type[k_type](new_input)
                    accepted = True
                    self.result_json[key] = new_input

                except Exception as error:
                    print('%s %s %s' % ('ERROR:', str(error), 'Please provide'
                                                              ' a new value '
                                                              'or skip key.'))
                    accepted = False

        return new_input

    def _introduce_object(self, key_type, key):
        """Print to user the object being iterated."""
        _type = key_type
        if key_type == 'empty':
            _type = 'object'
        self._print_interactive('Creating a [%s] named [%s].' % (_type, key))

    def _get_random_value(self, my_type):
        """Return random value from pool, based on provided type."""
        value_pool = self.RANDOM_POOL[my_type]
        max_range = len(value_pool)
        number = random.randint(0, max_range - 1)

        return value_pool[number]

    def _accumulate_cursor(self, current_cursor_inx, new_array=False):
        """Update the result cursor collection with the key being iterated."""

        line = ''
        for item in self.result_cursor:
            line = line + '[%s]' % str(item)
        self.result_cursor_collection.append(line)
        self.result_cursor.pop(current_cursor_inx)
        if new_array:
            self.result_cursor.pop(current_cursor_inx - 1)

    def _add_object_oriented(self, key, value):
        """Place the new object in the correct location oriented by cursor."""
        result = self.result_builder

        for level in self.result_cursor:
            result = result[level]

        result[key] = value

        return result


def open_doc():
    """Read json schema sample for test iteration."""
    the_doc = 'samples/multi_use'

    with open(the_doc, 'r') as doc:
        my_doc = json.load(doc)

    return my_doc

