import 'package:flutter/material.dart';
import 'package:yike_mobile_app/Widgets/cce_assigned.dart';
import 'package:yike_mobile_app/Widgets/complaint_timline.dart';
import 'package:yike_mobile_app/Widgets/complint_form.dart';

import 'chatpage.dart';

class ComplaintDetails extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    return _CompliantDetailsState();
  }
}

class _CompliantDetailsState extends State<ComplaintDetails> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            Expanded(
              child: Text(
                "#RedGear0001",
                style: TextStyle(
                  color: Colors.white,
                  fontSize: 20,
                ),
                textAlign: TextAlign.center,
              ),
            ),
            InkWell(child: Text(
              "Help",
              style: TextStyle(fontSize: 16, color: Colors.white),
            ),
            onTap: (){
              Navigator.push(context,MaterialPageRoute(builder: (context) => ChatPage()));
            },
            ),
            
          ],
        ),
      ),
      body: ListView(children: <Widget>[
        ComplaintTimline(),
        AssignedCCE(),
        ComplaintForm(),
      ],),
    );
  }
}
