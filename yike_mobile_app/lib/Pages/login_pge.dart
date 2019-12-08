import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:yike_mobile_app/Pages/complaits.dart';
import 'package:yike_mobile_app/Pages/register.dart';
import 'dart:convert';
import 'package:yike_mobile_app/Widgets/Buttons/raised_gradient_button.dart';
import 'package:yike_mobile_app/Widgets/Buttons/signup_button.dart';
import 'package:yike_mobile_app/Widgets/TextFields/custom_tff.dart';
import 'package:yike_mobile_app/Widgets/TextFields/password.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LoginPage extends StatelessWidget {
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final String paSwd0="";
  final String eMail0="";
  getData(context) async {
    String paSwd = passwordController.text;
    print(paSwd);
    print(eMail0);
    String eMail = emailController.text;
    String url = 'http://10.0.34.121:8000/api/tokenpair/?format=json';
    Map<String, String> headers = {"Content-type": "application/json"};
    String json0 = '{"password": "' + paSwd + '", "email": "' + eMail + '"}';
    Response response = await post(url, headers: headers, body: json0);
    int statusCode = response.statusCode;
    if (statusCode == 200) {
      Map<String, dynamic> data = json.decode(response.body);
      print(data);

      if (data["message"] == "Successful") {
        await addStringToSF("email", eMail, "string");
        await addStringToSF("password", paSwd, "string");
        await addStringToSF("token", data["token"], "string");
        await addStringToSF("refresh_token", data["refresh_token"], "string");
        await addStringToSF("logged", true, "bool");

        Navigator.pushReplacement(
            context, MaterialPageRoute(builder: (context) => ComplaintPage()));
      }
      else {
        var alertStyle = AlertStyle(
          animationType: AnimationType.fromTop,
          isCloseButton: false,
          isOverlayTapDismiss: false,
          descStyle: TextStyle(fontWeight: FontWeight.normal,fontSize: 14),
          animationDuration: Duration(milliseconds: 400),
          alertBorder: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(0.0),
            side: BorderSide(
              color: Colors.grey,
            ),
          ),
          titleStyle: TextStyle(
            color: Colors.red,
          ),
        );
        Alert(
          context: context,
          style: alertStyle,
          type: AlertType.error,
          title: "Login Failed",
          desc: "Something went wrong",
          buttons: [
            DialogButton(
              child: Text(
                "Try Again",
                style: TextStyle(color: Colors.white, fontSize: 20),
              ),
              onPressed: () => Navigator.pop(context),
              color: Color.fromRGBO(245, 88, 88, 1.0),
              radius: BorderRadius.circular(10.0),
            ),
          ],
        ).show();
      }
    }
  }

  getValuesSF(String key, String tYpe) async {
    if (tYpe.toLowerCase() == "string") {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      return prefs.getString(key);
    } else if (tYpe.toLowerCase() == "integer") {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      return prefs.getString(key);
    }
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString(key);
  }

  tryLogin(context) {
    getData(context);
  }

  addStringToSF(String key, vaLue, String tYpe) async {
    print("this is awesome");
    if (tYpe.toLowerCase() == "string") {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      prefs.setString(key, vaLue);
    } else if (tYpe.toLowerCase() == "integer") {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      prefs.setInt(key, vaLue);
    } else if (tYpe.toLowerCase() == "bool") {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      prefs.setBool(key, vaLue);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView(
        children: <Widget>[
          Container(
              margin: EdgeInsets.fromLTRB(16, 50, 16, 4),
              child: Text(
                "Welcome Back",
                style: TextStyle(
                    fontSize: 36,
                    color: Colors.indigo,
                    fontWeight: FontWeight.bold),
              )),
          Container(
            margin: EdgeInsets.fromLTRB(16, 0, 16, 0),
            child: Text("Log in to complaint about your issues",
                style: TextStyle(fontSize: 16, color: Colors.black87)),
          ),
          Padding(
            padding: EdgeInsets.only(top: 32, left: 16, right: 16, bottom: 16),
            child: CustomTextFormField(
              hint: "Enter your Email Address",
              label: "Email Address",
              val: eMail0,
              controlleR: emailController,
            ),
          ),
          Padding(
            padding: EdgeInsets.only(left: 16, right: 16, top: 0, bottom: 16),
            child: PasswordField(
              controlleR: passwordController,
            ),
          ),
          Container(
            margin: EdgeInsets.only(top: 16, right: 16, left: 16),
            height: 50,
            child: RaisedGradientButton(
              gradient: LinearGradient(colors: <Color>[
                Color.fromRGBO(70, 70, 255, 1),
                Colors.indigo
                /*Colors.purple,
                Colors.purpleAccent,
                Colors.red,
                Colors.redAccent*/
              ]),
              child: Text(
                "Login",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 18,
                ),
              ),
              onPressed: () => tryLogin(context),
            ),
          ),
          Row(
            children: <Widget>[
              Container(
                child: Text(
                  "Forgot Password ?",
                  style: TextStyle(color: Colors.blueAccent, fontSize: 16),
                ),
                margin: EdgeInsets.only(top: 20, right: 16),
              ),
            ],
            mainAxisAlignment: MainAxisAlignment.end,
          ),
          Row(
            children: <Widget>[
              Container(
                margin: EdgeInsets.only(top: 20),
                child: Text(
                  "OR",
                  style: TextStyle(color: Colors.black38, fontSize: 18),
                ),
              ),
            ],
            mainAxisAlignment: MainAxisAlignment.center,
          ),
          SignupButton(
            onpressed: () {
              Navigator.push(context,
                  MaterialPageRoute(builder: (context) => RegisterPage()));
            },
            icon: Icon(
              Icons.email,
              size: 30,
              color: Colors.white,
            ),
            tittle: Text(
              "Sign up with Email",
              style: TextStyle(fontSize: 16, color: Colors.white),
            ),
          )
        ],
      ),
    );
  }
}
