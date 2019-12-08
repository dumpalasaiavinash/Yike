import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:http/http.dart';
import 'package:rflutter_alert/rflutter_alert.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:yike_mobile_app/Pages/add_complaint.dart';
import 'package:yike_mobile_app/Pages/profile.dart';
import 'dart:async';
import 'package:yike_mobile_app/Widgets/complaint_card.dart';

class ComplaintPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    return _ComplaintPageState();
  }
}

class _ComplaintPageState extends State<ComplaintPage> {
  num _currentIndex = 0;
  bool failed = false;
  gettokken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString("token");
  }

  getRefreshtokken() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    return prefs.getString("refresh_token");
  }

  getToken() async {
    // String refreshTokken =
  }

  Future<List> getData() async {
    print("begin");
    List data;
    try {
      http.Response resp = await http.get(
          Uri.encodeFull(
              "http://10.0.54.2:8000/api/getActiveComplaint/?format=json"),
          headers: {
            'Authorization': await gettokken(),
            "Accept": "application/json"
          }).timeout(Duration(seconds: 10));
      //print(resp.body);
      print(resp.statusCode);
      if (resp.statusCode == 200) {
        print(resp.body);
        if (resp.body == "{\"status\":203}"){
          http.Response resp0 = await http.post(
              "http://10.0.54.2:8000/api/refreshToken/?format=json",
              headers: {"Content-type": "application/json"},
              body: '{"refresh_token":"' + await getRefreshtokken() + '"}').timeout(Duration(seconds: 10));
        print(resp0.statusCode);
        if (resp0.statusCode == 200) {
          print(resp0.body);
        }
      }
        data = json.decode(resp.body);
        data.add(2);
      }
    } on TimeoutException catch (_) {
      print("LOL0");
      var alertStyle = AlertStyle(
        animationType: AnimationType.fromTop,
        isCloseButton: false,
        isOverlayTapDismiss: false,
        descStyle: TextStyle(fontWeight: FontWeight.normal, fontSize: 14),
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
      failed = await Alert(
        context: context,
        style: alertStyle,
        type: AlertType.error,
        title: "Server Connection Failed",
        desc: "Something went wrong",
        buttons: [
          DialogButton(
            child: Text(
              "Try Again",
              style: TextStyle(color: Colors.white, fontSize: 20),
            ),
            onPressed: () {
              Navigator.pop(context, true);
            },
            color: Color.fromRGBO(245, 88, 88, 1.0),
            radius: BorderRadius.circular(10.0),
          ),
        ],
      ).show();
      data.add(1);
    }

    return data;
  }

  Future<List> getData2() async {
    print("al");
    Future<List> data = (await getData()) as Future<List>;
    print("Failed");
    if (failed == true) {
      print("walla");
    }
    print(data);
    if (data == null) {
      print("DJ");
      await getToken();
    }
    return data;
  }

  _children(BuildContext context, num index) {
    if (index == 0)
      return DefaultTabController(
        length: 2,
        child: Scaffold(
            floatingActionButton: FloatingActionButton(
              onPressed: () {
                Navigator.push(context,
                    MaterialPageRoute(builder: (context) => AddComplaint()));
              },
              backgroundColor: Colors.white,
              child: Icon(
                Icons.add,
                color: Colors.blue,
                size: 32,
              ),
            ),
            appBar: AppBar(
              title: Row(
                children: <Widget>[
                  Text(
                    "My Complaints",
                    style: TextStyle(color: Colors.white, fontSize: 20),
                  )
                ],
                crossAxisAlignment: CrossAxisAlignment.center,
                mainAxisAlignment: MainAxisAlignment.center,
              ),
              bottom: TabBar(
                tabs: <Widget>[
                  Tab(
                    text: "Complaints",
                  ),
                  Tab(
                    text: "History",
                  )
                ],
              ),
            ),
            body: FutureBuilder(
              initialData: {},
              future: getData2(),
              builder: (BuildContext context, AsyncSnapshot snap) {
                print(snap.data);
                if (snap.data != null) {
                  return ListView.builder(
                    itemCount: snap.data.length,
                    itemBuilder: (BuildContext context, int index) {
                      return ComplaintCard(
                        prob: snap.data[index]['prob'],
                        complN: snap.data[index]['compN'],
                        org_name: snap.data[index]['org'],
                        haveprob: snap.data[index]['haveprob'],
                        compl: snap.data[index]['compl'],
                        date: snap.data[index]['date'],
                        time: snap.data[index]['time'],
                        comp_date: snap.data[index]['compDate'],
                        status: snap.data[index]['status'],
                      );
                    },
                  );
                } else if (snap.data == null) {
                  return Center(
                    child: Text(" No Complaint Found "),
                  );
                }
                return Center(
                  child: Text(" No Complaint Found "),
                );
              },
            )),
      );
    else
      return ProfilPage();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      bottomNavigationBar: BottomNavigationBar(
          onTap: onTabTapped, // new
          currentIndex: _currentIndex,
          items: [
            BottomNavigationBarItem(
                icon: Icon(Icons.home), title: Text("Home")),
            BottomNavigationBarItem(
                title: Text("Profile"), icon: Icon(Icons.person))
          ]),
      body: _children(context, _currentIndex),
    );
  }

  void onTabTapped(int index) {
    setState(() {
      _currentIndex = index;
    });
  }
}
