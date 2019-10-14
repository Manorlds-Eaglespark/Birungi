


class Helpers:
    @staticmethod
    def convert_array_to_JSON_one_product(data_array):
        return {
            "id": data_array[0],
            "name":data_array[1],
            "price":data_array[2],
            "brand":data_array[3],
            "category":data_array[4],
            "description":data_array[5],
            "pic_1":data_array[6],
            "pic_2":data_array[7],
            "pic_3":data_array[8],
            "pic_4":data_array[9],
            "time_added":data_array[10]
        }

    @staticmethod
    def convert_array_to_JSON_many_products(data_arrays):
        products = []
        for data_array in data_arrays:
            product = {
                "id": data_array[0],
                "name": data_array[1],
                "price": str(data_array[2]),
                "brand": data_array[3],
                "category": str(data_array[4]),
                "description": data_array[5],
                "pic_1": data_array[6],
                "pic_2": data_array[7],
                "pic_3": data_array[8],
                "pic_4": data_array[9],
                "time_added": data_array[10]
            }
            products.append(product)
        return products

    @staticmethod
    def convert_array_to_JSON_category(data_array):
        return {
            "id": data_array[0],
                "name": data_array[1],
                "price": str(data_array[2]),
                "brand": data_array[3],
                "category": str(data_array[4]),
                "description": data_array[5],
                "pic_1": data_array[6],
                "pic_2": data_array[7],
                "pic_3": data_array[8],
                "pic_4": data_array[9],
                "time_added": data_array[10]
        }
    
    def convert_category_array_to_JSON(data_array):
        categories = []
        for category in data_array:
            data = {
                "id": category[0],
                "name":category[1],
                "description":category[2],
                "icon_image":category[3],
                "created_on":category[4]
            }
            categories.append(data)
        return categories
