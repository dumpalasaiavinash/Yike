import 'package:flutter/material.dart';
import 'package:yike_mobile_app/Pages/complaits.dart';
import 'package:yike_mobile_app/Pages/register.dart';
import 'package:yike_mobile_app/Widgets/Buttons/raised_gradient_button.dart';
import 'package:yike_mobile_app/Widgets/Buttons/signup_button.dart';
import 'package:yike_mobile_app/Widgets/TextFields/custom_tff.dart';
import 'package:yike_mobile_app/Widgets/TextFields/password.dart';

class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView(
        children: <Widget>[
          //Container(child: Row(children: <Widget>[
          //Image.asset("assets/yikelogo.png",width:120,height: 120),],mainAxisAlignment: MainAxisAlignment.center,),
          //margin: EdgeInsets.only(top:40),),
          Container(
              margin: EdgeInsets.fromLTRB(16, 50, 16, 4),
              child: Text(
                "Welcome",
                style: TextStyle(
                    fontSize: 36,
                    color: Color.fromRGBO(70, 70, 255, 1),
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
              val: "",
            ),
          ),
          Padding(
            padding: EdgeInsets.only(left: 16, right: 16, top: 0, bottom: 16),
            child: Password(),
          ),
          Container(
            margin: EdgeInsets.only(top: 16, right: 16, left: 16),
            height: 50,
            child: RaisedGradientButton(
              gradient: LinearGradient(colors: <Color>[
                Color.fromRGBO(70, 70, 255, 1),
                Color.fromRGBO(80, 80, 245, 1)
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
              onPressed: () {
                
                Navigator.pushReplacement(context,  MaterialPageRoute(builder: (context) => ComplaintPage()));
              },
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
            onpressed:(){ Navigator.push(context, MaterialPageRoute(builder: (context) => RegisterPage()));},
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
