import "package:flutter/material.dart";
import 'package:yike_mobile_app/Widgets/Buttons/raised_gradient_button.dart';
import 'package:yike_mobile_app/Widgets/TextFields/custom_tff.dart';
import 'package:yike_mobile_app/Widgets/TextFields/password.dart';
import 'package:yike_mobile_app/Widgets/checkbox.dart';

class RegisterPage extends StatelessWidget {
  bool _checked = false;
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Scaffold(
     body:ListView(
      children: <Widget>[

        Container(
          margin: EdgeInsets.fromLTRB(16, 50, 16, 4),
            child: Text(
          "Welcome",
          style: TextStyle(fontSize: 36, color:  Color.fromRGBO(70, 70, 255, 1), fontWeight: FontWeight.bold),
        )),
        Container(margin: EdgeInsets.fromLTRB(16, 0, 16, 0),
        child: Text("Register to complaint about your issues",style:TextStyle(fontSize: 16,color: Colors.black87)),
        ),

        Container(
          margin: EdgeInsets.only(top: 32, left: 16, right: 16, bottom: 16),
          child: CustomTextFormField(
            val: "",
            hint: "Enter your Name",
            label: "User Name",
          ),
        ),
        Container(
          margin: EdgeInsets.only(top: 0, right: 16, left: 16, bottom: 16),
          child: CustomTextFormField(
            val: "",
            hint: "Enter your Email Address",
            label: "Email Address",
          ),
        ),
        Container(
          margin: EdgeInsets.only(top: 0, right: 16, left: 16, bottom: 16),
          child: PasswordField(),
        ),
        Container(
          margin: EdgeInsets.only(top: 0, right: 16, left: 12, bottom: 16),
          child: Row(
            children: <Widget>[
              YikeCheckBox(),
              Text(
                "I agree on all of ",
                style: TextStyle(color: Colors.black38),
              ),
              Text(" terms & condition .",
                  style: TextStyle(color: Colors.blueAccent)),
            ],
          ),
        ),
        Container(
          margin: EdgeInsets.only(left: 16,right: 16),
          child: RaisedGradientButton(
            onPressed: () {},
            gradient: LinearGradient(colors: <Color>[
              Color.fromRGBO(70, 70, 255, 1),
              Color.fromRGBO(70, 70, 255, 1),

            ]),
            child: Text("Register", style: TextStyle(color: Colors.white,fontSize: 16)),
          ),
        ),
      ],
    ),);
  }
}
