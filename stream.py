# from keras.preprocessing.image import load_img,img_to_array
# import numpy as np
# from keras.models import load_model

# model=load_model('./BC.h5',compile=False)
# lab={}
# def processed_img(img_path):
#     img=load_img(img_path,target_size=(224,224,3))
#     img=img_to_array(img)
#     img=img/255
#     img=np.expand_dims(img,[0])
#     answer=model.predict(img)
#     y_class=answer.argmax(axis=-1)
#     print(y_class)
#     y=" ".join(str(x) for x in y_class)
#     y=int(y)
#     res=lab[y]
#     print(res)
