import React, { useState } from 'react';
import {
  SafeAreaView,
  Image,
  StatusBar,
  StyleSheet,
  Text,
  Platform,
  Dimensions,
  useColorScheme,
  View,
  TouchableOpacity,
  ImageBackground,
  Modal,
  ScrollView,
  Button,
} from 'react-native';
import axios from 'axios';
import { launchCamera, launchImageLibrary } from 'react-native-image-picker';
import { Colors } from 'react-native/Libraries/NewAppScreen';
import PermissionsService, {isIOS} from './Permissions';

axios.interceptors.request.use(
  async (config) => {
    let request = config;
    console.log(request);
    request.headers = {
      'Content-Type': 'multipart/form-data',
      Accept: 'text/plain',
    };
    request.url = configureUrl(config.url);
    return request;
  },
  (error) => error
);

export const { height, width } = Dimensions.get('window');

export const configureUrl = (url) => {
  let authUrl = url;
  if (url && url[url.length - 1] === '/') {
    authUrl = url.substring(0, url.length - 1);
  }
  return authUrl;
};

export const fonts = {
  Bold: { fontFamily: 'Roboto-Bold' },
};

const options = {
  mediaType: 'photo',
  quality: 1,
  width: 256,
  height: 256,
  includeBase64: true,
};


const App = () => {
  const [result, setResult] = useState('');
  const [label, setLabel] = useState('');
  const isDarkMode = useColorScheme() === 'dark';
  const [image, setImage] = useState('');
  const [showSolution, setShowSolution] = useState(false);
  const [solution, setSolution] = useState('');

  const backgroundStyle = {
    backgroundColor: isDarkMode ? Colors.darker : Colors.lighter,
  };

  const getPrediction = async (params) => {
    try {
      const formData = new FormData();
      formData.append('file', params);
      const API_URL = 'http://192.168.35.186:8000/predict';
      const url = configureUrl(API_URL);
      const response = await axios.post(url, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.log(error);
      throw new Error('Failed to predicting.');
    }
  };
  
  const toggleSolutionModal = () => {
    setShowSolution(!showSolution);
  }

  const manageCamera = async (type) => {
    try {
      if (!(await PermissionsService.hasCameraPermission())) {
        return [];
      } else {
        if (type === 'Camera') {
          openCamera();
        } else {
          openLibrary();
        }
      }
    } catch (err) {
      console.log(err);
    }
  };

  const openCamera = async () => {
    launchCamera(options, async (response) => {
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
      } else {
        const uri = response?.assets[0]?.uri;
        const path = Platform.OS !== 'ios' ? uri : 'file://' + uri;
        getResult(path, response);
      }
    });
  };

  const clearOutput = () => {
    setResult('');
    setImage('');
    setSolution('');
  };

  const getResult = async (path, response) => {
    setImage(path);
    setLabel('Predicting...');

    const params = {
      uri: path,
      type: response.assets[0].type,
      name: response.assets[0].fileName,
    };

    try {
      const res = await getPrediction(params);
      console.log(res.class);
      console.log(res.confidence);
      setLabel(res.class);
      setResult(res.confidence);
      setSolution(res.solution);
    } catch (error) {
      console.log(error);
      setLabel('Failed to predict');
    }
  };
  

  const openLibrary = async () => {
    launchImageLibrary(options, async (response) => {
      if (response.didCancel) {
        console.log('User cancelled image picker');
      } else if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else if (response.customButton) {
        console.log('User tapped custom button: ', response.customButton);
      } else {
        const uri = response.assets[0].uri;
        const path = Platform.OS !== 'ios' ? uri : 'file://' + uri;
        getResult(path, response);
      }
    });
  };
  
  return (
    <SafeAreaView style={[backgroundStyle, styles.outer]}>
      <StatusBar barStyle={isDarkMode ? 'light-content' : 'dark-content'} />
      <ImageBackground
        blurRadius={10}
        source={require('./assets/background1.jpg')}
        style={{height: height, width: width}}
      />
      <Text style={styles.title}>{'Orange Disease \n Prediction App'}</Text>
      <TouchableOpacity onPress={clearOutput} style={styles.clearStyle}>
        <Image source={{uri: 'clean'}} style={styles.clearImage} />
      </TouchableOpacity>
      {(image?.length && (
        <Image source={{uri: image}} style={styles.imageStyle} />
      )) ||
        null}
      {(result && label && (
        <View style={styles.mainOuter}>
          <Text style={[styles.space, styles.labelText]}>
            {'Label: \n'}
            <Text style={styles.resultText}>{label}</Text>
          </Text>
          <Text style={[styles.space, styles.labelText]}>
            {'Confidence: \n'}
            <Text style={styles.resultText}>
              {parseFloat(result).toFixed(2) + '%'}
            </Text>
          </Text>
        </View>
      )) ||
        (image && <Text style={styles.emptyText}>{label}</Text>) || (
          <Text style={styles.emptyText}>
            Use below buttons to select a picture of a orange plant.
          </Text>
        )}
      <View style={styles.btn}>
        <TouchableOpacity
          activeOpacity={0.9}
          onPress={() => manageCamera('Camera')}
          style={styles.btnStyle}>
          <Image source={{uri: 'camera'}} style={styles.imageIcon} />
        </TouchableOpacity>
        <TouchableOpacity
          activeOpacity={0.9}
          onPress={() => manageCamera('Photo')}
          style={styles.btnStyle}>
          <Image source={{uri: 'gallery'}} style={styles.imageIcon} />
        </TouchableOpacity>
        <TouchableOpacity onPress={toggleSolutionModal} style={styles.btnStyle}>
          <Text style={styles.buttonText}>Solution</Text>
        </TouchableOpacity>
      </View>
        <Modal visible={showSolution} animationType="slide">
         <SafeAreaView>
           <ScrollView>
             <View style={styles.solutionContainer}>
               <Text style={styles.solutionText}>Treatment: {solution}</Text>
             </View>
             <Button title="Close" onPress={toggleSolutionModal} />
           </ScrollView>
         </SafeAreaView>
       </Modal>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  title: {
    alignSelf: 'center',
    position: 'absolute',
    top: (isIOS && 35) || 10,
    fontSize: 30,
    ...fonts.Bold,
    color: '#FFF',
  },
  clearImage: {height: 40, width: 40, tintColor: '#FFF'},
  mainOuter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    position: 'absolute',
    top: height / 1.6,
    alignSelf: 'center',
  },
  outer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  btn: {
    position: 'absolute',
    bottom: 40,
    justifyContent: 'space-between',
    flexDirection: 'row',
  },
  btnStyle: {
    backgroundColor: '#FFF',
    opacity: 0.8,
    margin: 20,
    padding: 20,
    borderRadius: 20,
    alignItems: 'center',
    justifyContent: 'center',
  },
  imageStyle: {
    marginBottom: 50,
    width: width / 1.5,
    height: width / 1.5,
    borderRadius: 20,
    position: 'absolute',
    borderWidth: 0.3,
    borderColor: '#FFF',
    top: height / 4.5,
  },
  clearStyle: {
    position: 'absolute',
    top: 100,
    right: 30,
    tintColor: '#FFF',
    zIndex: 10,
  },
  space: {marginVertical: 10, marginHorizontal: 10},
  labelText: {color: '#FFF', fontSize: 15, ...fonts.Bold},
  resultText: {fontSize: 17, ...fonts.Bold},
  imageIcon: {height: 40, width: 40, tintColor: '#000'},
  emptyText: {
    position: 'absolute',
    top: height / 1.6,
    alignSelf: 'center',
    color: '#FFF',
    fontSize: 16,
    maxWidth: '70%',
    ...fonts.Bold,
  },
  buttonText: {
    color: 'black',
    fontSize: 20,
    ...fonts.Bold,
    textAlign: 'center',
    textShadowColor: 'rgba(0, 0, 0, 0.5)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  },
  solutionContainer: {
    marginVertical: 20,
    paddingHorizontal: 20,
  },
  solutionText: {
    fontSize: 18,
    ...fonts.Bold,
    textAlign: 'center',
    marginTop: 10,
    color: '#A9A9A9',
  },
});

export default App;