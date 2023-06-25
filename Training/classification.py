from keras import models,layers

class CNN:

    def Classification(self,input_shape,n_classes):
        input_shape=input_shape
        n_classes=n_classes

        model=models.Sequential([
            layers.InputLayer(input_shape=input_shape),
            layers.Conv2D(32,(3,3),activation='relu'),
            layers.MaxPooling2D((2,2)),
            layers.Conv2D(64,kernel_size=(3,3),activation='relu'),
            layers.MaxPooling2D((2,2)),
            layers.Conv2D(64,kernel_size=(3,3),activation='relu'),
            layers.MaxPooling2D((2,2)),
            layers.Conv2D(64,(3,3),activation='relu'),
            layers.MaxPooling2D((2,2)),
            layers.Conv2D(64,(3,3),activation='relu'),
            layers.MaxPooling2D((2,2)),
            layers.Conv2D(64,(3,3),activation='relu'),
            layers.MaxPooling2D((2,2)),
            layers.Flatten(),
            layers.Dense(64,activation='relu'),
            layers.Dense(n_classes,activation='softmax')
        ])

        model.build(input_shape=input_shape)

        model.summary()

        return model
    
    def Solution(self,pred_disease):
        if pred_disease == 'Black__Spot__fruits' or pred_disease == "Black__Spot__leaves":
            return '\n\n\n a. Remove the leaf litter from beneath trees and cover it to compost. \n b. Prune out dead wood and double bag and place it in waste receptacle. \n c. Chemical control with copper applications from May to October.'

        elif pred_disease == 'Citrus__Canker__fruits' or pred_disease == "Citrus__Canker__leaves":
            return '\n\n\n a. If the disease is introduced in area, all infected trees should be removed and destroyed. \n b. In areas where disease is endemic, windbreaks can help to reduce severity. \n c. Cultural control of disease should focus on controlling leaf miner populations, utilizing wind breaks and application of copper spray.'

        elif pred_disease == 'Citrus__Scab__fruits':
            return '\n\n\n a. Prune out heavily infected section of tree \n b. Chemical control with copper products. \n i. 1st application: Spring flush half-expanded. \n ii. 2nd application: Petal fall. \n iii. 3rd application: 2 weeks post-petal fall.'

        elif pred_disease == 'Healthy__fruits' or pred_disease == "Healthy__leaves":
            return '\n\n\n Requires no treatment but should maintain with proper tree hygiene with regular checkups.'

        elif pred_disease == 'Huanglongbing__fruits' or pred_disease == "Huanglongbing__leaves":
            return '\n\n\n a. Once the tree become infected with HLB, it cannot be cured. \n b. Control is therefore, a reliant on preventing the disease occurring in the first place and this is achieved through strict quarantining to prevent the introduction of citrus psylids to area which are currently free of pest.'

        else:
            return "\n\n\n a. Minimize dead wood in canopy and dispose of dead wood with yard waste. \n b. Grapefruit is particularly susceptible but do not harm edibility of fruit \n Use copper application as the best chemical control in late April and continue to mid-July every 21 days."
