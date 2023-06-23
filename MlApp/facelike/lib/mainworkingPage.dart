// ignore_for_file: deprecated_member_use

import 'package:facelike/home.dart';
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';
import 'dart:convert';
import 'package:path_provider/path_provider.dart';
import 'package:flutter/widgets.dart';
import 'package:http_parser/http_parser.dart';
import 'package:permission_handler/permission_handler.dart';

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.name});

  final String name;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int _counter = 0;

  void _incrementCounter() {
    //  wriet your code here about image picker
  }
  // File _imageFile = File('assets/image.jpg');

  late File _imageFile;
  late File _imageFile_output;
  late var _name = "";
  // late File _imageFile_output;
  bool isshow = false;
  bool isbackhomepage = false;
  String url = 'http://10.0.2.2:8000/upload/';
  Future<void> getPermission() async {
    await Permission.camera.request();
    await Permission.photos.request();
  }

  Future<void> _pickImage(ImageSource source) async {
    final PermissionStatus cameraStatus = await Permission.camera.status;
    final PermissionStatus photosStatus = await Permission.photos.status;

    if (!cameraStatus.isGranted || !photosStatus.isGranted) {
      await getPermission();
    }

    final pickedImage = await ImagePicker().getImage(source: source);

    print("################################");
    print(pickedImage?.path);
    print(pickedImage);
    if (pickedImage != null) {
      setState(() {
        _imageFile = File(pickedImage.path);

        isbackhomepage = true;
      });

      // Perform the asynchronous operation outside of setState
      try {
        print(pickedImage.path);
        var imageFile =
            await http.MultipartFile.fromPath('image', pickedImage.path);
        var request = http.MultipartRequest('POST', Uri.parse(url));
        // Add the image file to the request
        request.files.add(imageFile);
        print("********************************");

        var streamedResponse = await request.send();
        // Send the request
        // Read the response
        var response = await http.Response.fromStream(streamedResponse);
        print(_imageFile);

        // Update the state with the obtained image URL

        if (response.statusCode == 200) {
          print('Image uploaded successfully');

          // Parse the response body as JSON
          var responseBody = jsonDecode(response.body);

          // Extract the image URL from the response
          var imageUrl = responseBody['image_url'];
          var name = responseBody['name'];
          print(imageUrl);
          // Make a GET request to fetch the image data
          var imageResponse = await http.get(Uri.parse(imageUrl));

          if (imageResponse.statusCode == 200) {
            final file =
                File('${(await getTemporaryDirectory()).path}/temp.jpg');

            // Write the image data to the file
            await file.writeAsBytes(imageResponse.bodyBytes);

            setState(() {
              _imageFile_output = file;
              isshow = true;
              _name = name;
            });
          } else {
            throw Exception('Failed to load image');
          }
        } else {
          throw Exception('Failed to upload image');
        }
      } catch (error) {
        // Handle any errors that occurred during the asynchronous operation
        print('Error: $error');
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Text(_name.toString()),
            Row(
              children: [
                Expanded(
                  child: isshow != false
                      ? Image.file(
                          _imageFile,
                          width: 150,
                          height: 150,
                        )
                      : Container(),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: isshow != false
                      ? Image.file(
                          _imageFile_output,
                          width: 150,
                          height: 150,
                        )
                      : Container(),
                ),
              ],
            ),
          ],
        ),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      floatingActionButton: FloatingActionButton(
        onPressed: _incrementCounter,
        tooltip: 'Image',
        child: GestureDetector(
          onTap: () {
            if (isbackhomepage) {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => LoginPage()),
              );
            } else {
              showDialog(
                  context: context,
                  builder: (context) => AlertDialog(
                        title: Text('Select an Image'),
                        content: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            ListTile(
                              leading: Icon(Icons.photo_library),
                              title: Text('Gallery'),
                              onTap: () {
                                _pickImage(ImageSource.gallery);
                                Navigator.of(context).pop();
                              },
                            ),
                            ListTile(
                              leading: Icon(Icons.camera_alt),
                              title: Text('Camera'),
                              onTap: () {
                                _pickImage(ImageSource.camera);
                                Navigator.of(context).pop();
                              },
                            ),
                          ],
                        ),
                      ));
            }
          },
          child: isbackhomepage != true
              ? Icon(Icons.image)
              : Icon(Icons.back_hand),
        ),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
