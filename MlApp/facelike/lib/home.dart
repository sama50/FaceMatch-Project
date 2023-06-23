import 'package:facelike/mainworkingPage.dart';
import 'package:flutter/material.dart';

class LoginPage extends StatelessWidget {
  final _formKey = GlobalKey<FormState>();
  String? _name;
  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Form(
        key: _formKey,
        child: Scaffold(
          body: Container(
            margin: EdgeInsets.all(24),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _header(context),
                _inputField(context),
              ],
            ),
          ),
        ),
      ),
    );
  }

  _header(context) {
    return Column(
      children: [
        const Text(
          "Your Face Meatch",
          style: TextStyle(fontSize: 34, fontWeight: FontWeight.bold),
        ),
        Text("see which celrebity looks like you"),
      ],
    );
  }

  _inputField(context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        TextFormField(
          decoration: InputDecoration(
              hintText: "name",
              border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(18),
                  borderSide: BorderSide.none),
              fillColor: Theme.of(context).primaryColor.withOpacity(0.1),
              filled: true,
              prefixIcon: const Icon(Icons.person)),
          validator: (value) {
            if (value!.isEmpty) {
              return 'Please enter Name';
            }
            _name = value;
            return null;
          },
        ),
        const SizedBox(height: 10),
        SizedBox(height: 10),
        ElevatedButton(
          onPressed: () {
            if (_formKey.currentState!.validate()) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: const Text('Processing...')),
              );
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => MyHomePage(
                          name: _name.toString(),
                        )),
              );
              // Add your registration logic here
            }
          },
          child: Text(
            "Check",
            style: TextStyle(fontSize: 20),
          ),
          style: ElevatedButton.styleFrom(
            shape: StadiumBorder(),
            padding: EdgeInsets.symmetric(vertical: 16),
          ),
        )
      ],
    );
  }

  _forgotPassword(context) {
    return TextButton(onPressed: () {}, child: Text("Forgot password?"));
  }

  _signup(context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text("Dont have an account? "),
        // TextButton(
        //     onPressed: () {
        //       Navigator.push(
        //         context,
        //         MaterialPageRoute(builder: (context) => RegisterPage()),
        //       );
        //     },
        //     child: const Text("Sign Up"))
      ],
    );
  }
}
