import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:yike_mobile_app/webview_flutter.dart';

class Complaint_Form extends StatelessWidget{
  final String formId;
  Complaint_Form({this.formId});
  final String userEmail =  'yashukikkuri@gmail.com';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: WebView(initialUrl: "https://www.google.com",),
    );
  }
}
  getuserEmail() async{
    return await getuseremail();
  }

 getuseremail() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString("token");
  }