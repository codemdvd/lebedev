db.createCollection('wine', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            properties: {
                article: {
                    bsonType: 'string',
                    description: 'Product unique article',
                    maximum: 20
                },

                name: {
                    bsonType: 'string',
                    description: 'Name of product',
                    maximum: 100
                },

                country: {
                    bsonType: 'string',
                    description: 'Which country\' wine is it',
                    maximum: 40
                },

                manufactorer: {
                    bsonType: 'string',
                    description: 'Name of wine manufactorer',
                    maximum: 50
                },

                description: {
                    bsonType: 'string',
                    description: 'Description of wine',
                    maximum: 1000
                },

                price: {
                    bsonType: 'double',
                    decription: 'Pirce per item'
                },

                items_left: {
                    bsonType: 'int',
                    description: 'How many items left in store'
                },


                required: [
                    'article',
                    'name',
                    'country',
                    'manufactorer',
                    'description',
                    'price',
                    'items_left'
                ],

                title: 'Validation of wine collection'
            }
        }
    }
})


db.createCollection('cart', {
    validator: {
        $jsonSchema: {
            bsonType: 'object',
            properties: {
                client_username: {
                    bsonType: 'string',
                    description: 'Username of cart owner',
                    maximum: 30
                },

                cart_list: {
                    bsonType: 'list',
                    description: 'Cart consistance',
                    items: {
                        bsonType: 'object',
                        properties: {
                            wine: {
                                bsonType: 'objectId',
                                description: 'Reference to product'
                            },

                            amount: {
                                bsonType: 'int',
                                description: 'Amount of products in cart'
                            }
                        }
                    }
                },

                required: [
                    'client_username',
                    'cart_list'
                ],

                title: 'Validation of cart collection'
            }
        }
    }
})