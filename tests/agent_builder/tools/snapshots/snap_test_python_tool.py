# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_should_be_possible_to_override_defaults 1'] = {
    'binding': {
        'python': {
            'function': 'test_python_tool:my_tool'
        }
    },
    'description': 'the description',
    'input_schema': {
        'properties': {
        },
        'required': [
        ],
        'type': 'object'
    },
    'name': 'myName',
    'output_schema': {
        'properties': {
        }
    },
    'permission': 'ADMIN'
}

snapshots['test_should_support_pydantic_typed_args 1'] = {
    'binding': {
        'python': {
            'function': 'test_python_tool:sample_tool'
        }
    },
    'description': None,
    'input_schema': {
        'properties': {
            'b': {
                'properties': {
                    'a': {
                        'title': 'A',
                        'type': 'string'
                    },
                    'b': {
                        'anyOf': [
                            {
                                'type': 'string'
                            },
                            {
                                'type': 'null'
                            }
                        ],
                        'title': 'B'
                    },
                    'c': {
                        'default': None,
                        'title': 'C',
                        'type': 'string'
                    },
                    'd': {
                        'properties': {
                            'na': {
                                'title': 'Na',
                                'type': 'integer'
                            }
                        },
                        'required': [
                            'na'
                        ],
                        'title': 'Nested',
                        'type': 'object'
                    },
                    'e': {
                        'anyOf': [
                            {
                                'properties': {
                                    'na': {
                                        'title': 'Na',
                                        'type': 'integer'
                                    }
                                },
                                'required': [
                                    'na'
                                ],
                                'title': 'Nested',
                                'type': 'object'
                            },
                            {
                                'type': 'null'
                            }
                        ]
                    },
                    'f': {
                        'properties': {
                            'na': {
                                'title': 'Na',
                                'type': 'integer'
                            }
                        },
                        'required': [
                            'na'
                        ],
                        'title': 'Nested',
                        'type': 'object'
                    }
                },
                'required': [
                    'a',
                    'b',
                    'd',
                    'e'
                ],
                'title': 'SampleParamA',
                'type': 'object'
            },
            'sampleA': {
                'properties': {
                    'a': {
                        'title': 'A',
                        'type': 'string'
                    },
                    'b': {
                        'anyOf': [
                            {
                                'type': 'string'
                            },
                            {
                                'type': 'null'
                            }
                        ],
                        'title': 'B'
                    },
                    'c': {
                        'default': None,
                        'title': 'C',
                        'type': 'string'
                    },
                    'd': {
                        'properties': {
                            'na': {
                                'title': 'Na',
                                'type': 'integer'
                            }
                        },
                        'required': [
                            'na'
                        ],
                        'title': 'Nested',
                        'type': 'object'
                    },
                    'e': {
                        'anyOf': [
                            {
                                'properties': {
                                    'na': {
                                        'title': 'Na',
                                        'type': 'integer'
                                    }
                                },
                                'required': [
                                    'na'
                                ],
                                'title': 'Nested',
                                'type': 'object'
                            },
                            {
                                'type': 'null'
                            }
                        ]
                    },
                    'f': {
                        'properties': {
                            'na': {
                                'title': 'Na',
                                'type': 'integer'
                            }
                        },
                        'required': [
                            'na'
                        ],
                        'title': 'Nested',
                        'type': 'object'
                    }
                },
                'required': [
                    'a',
                    'b',
                    'd',
                    'e'
                ],
                'title': 'SampleParamA',
                'type': 'object'
            }
        },
        'required': [
            'sampleA'
        ],
        'type': 'object'
    },
    'name': 'sample_tool',
    'output_schema': {
        'properties': {
            'a': {
                'title': 'A',
                'type': 'string'
            },
            'b': {
                'anyOf': [
                    {
                        'type': 'string'
                    },
                    {
                        'type': 'null'
                    }
                ],
                'title': 'B'
            },
            'c': {
                'default': None,
                'title': 'C',
                'type': 'string'
            },
            'd': {
                'properties': {
                    'na': {
                        'title': 'Na',
                        'type': 'integer'
                    }
                },
                'required': [
                    'na'
                ],
                'title': 'Nested',
                'type': 'object'
            },
            'e': {
                'anyOf': [
                    {
                        'properties': {
                            'na': {
                                'title': 'Na',
                                'type': 'integer'
                            }
                        },
                        'required': [
                            'na'
                        ],
                        'title': 'Nested',
                        'type': 'object'
                    },
                    {
                        'type': 'null'
                    }
                ]
            },
            'f': {
                'properties': {
                    'na': {
                        'title': 'Na',
                        'type': 'integer'
                    }
                },
                'required': [
                    'na'
                ],
                'title': 'Nested',
                'type': 'object'
            }
        },
        'required': [
            'a',
            'b',
            'd',
            'e'
        ],
        'type': 'object'
    },
    'permission': 'READ_ONLY'
}

snapshots['test_should_support_typed_none_args 1'] = {
    'binding': {
        'python': {
            'function': 'test_python_tool:my_tool'
        }
    },
    'description': 'the description',
    'input_schema': {
        'properties': {
            'input': {
                'type': 'null'
            }
        },
        'required': [
        ],
        'type': 'object'
    },
    'name': 'myName',
    'output_schema': {
        'type': 'null'
    },
    'permission': 'ADMIN'
}

snapshots['test_should_support_typed_optional_args 1'] = {
    'binding': {
        'python': {
            'function': 'test_python_tool:my_tool'
        }
    },
    'description': 'the description',
    'input_schema': {
        'properties': {
            'input': {
                'type': 'string'
            }
        },
        'required': [
        ],
        'type': 'object'
    },
    'name': 'myName',
    'output_schema': {
        'anyOf': [
            {
                'type': 'string'
            },
            {
                'type': 'null'
            }
        ]
    },
    'permission': 'ADMIN'
}

snapshots['test_should_support_typed_typings_inputs_and_outputs 1'] = {
    'binding': {
        'python': {
            'function': 'test_python_tool:my_tool'
        }
    },
    'description': 'the description',
    'input_schema': {
        'properties': {
            'input': {
                'type': 'string'
            }
        },
        'required': [
            'input'
        ],
        'type': 'object'
    },
    'name': 'myName',
    'output_schema': {
        'type': 'string'
    },
    'permission': 'ADMIN'
}

snapshots['test_should_use_correct_defaults 1'] = {
    'binding': {
        'python': {
            'function': 'test_python_tool:my_tool'
        }
    },
    'description': None,
    'input_schema': {
        'properties': {
        },
        'required': [
        ],
        'type': 'object'
    },
    'name': 'my_tool',
    'output_schema': {
        'properties': {
        }
    },
    'permission': 'READ_ONLY'
}

snapshots['test_should_work_with_dicts 1'] = {
    'binding': {
        'python': {
            'function': 'test_python_tool:sample_tool'
        }
    },
    'description': None,
    'input_schema': {
        'properties': {
            'b': {
                'type': 'object'
            },
            'sampleA': {
                'type': 'object'
            }
        },
        'required': [
            'sampleA'
        ],
        'type': 'object'
    },
    'name': 'sample_tool',
    'output_schema': {
        'items': {
            'type': 'object'
        },
        'type': 'array'
    },
    'permission': 'READ_ONLY'
}

snapshots['test_should_work_with_lists 1'] = {
    'binding': {
        'python': {
            'function': 'test_python_tool:sample_tool'
        }
    },
    'description': None,
    'input_schema': {
        'properties': {
            'b': {
                'items': {
                    'type': 'string'
                },
                'type': 'array'
            },
            'sampleA': {
                'items': {
                    'type': 'string'
                },
                'type': 'array'
            }
        },
        'required': [
            'sampleA'
        ],
        'type': 'object'
    },
    'name': 'sample_tool',
    'output_schema': {
        'items': {
            'type': 'string'
        },
        'type': 'array'
    },
    'permission': 'READ_ONLY'
}
