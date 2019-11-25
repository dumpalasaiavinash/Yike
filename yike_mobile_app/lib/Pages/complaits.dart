import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:yike_mobile_app/Pages/add_complaint.dart';
import 'dart:async';

import 'package:yike_mobile_app/Widgets/complaint_card.dart';

class ComplaintPage extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    return _ComplaintPageState();
  }
}

class _ComplaintPageState extends State<ComplaintPage> {
  
  Future<List> getData() async {
    print("begin");
    http.Response resp = await http.get(
        Uri.encodeFull("http://10.0.34.121:8000/complaints/?format=json"),
        headers: {"Acce pt": "application/json"});
    //print(resp.body);
    List data = json.decode(resp.body);
    return data;
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    
    return DefaultTabController(
        length: 2,
        child: Scaffold(
          bottomNavigationBar: BottomNavigationBar(
            items: [
              BottomNavigationBarItem(
                icon: Icon(Icons.home),
                title: Text("My Complaints")
              ),
              BottomNavigationBarItem(
                icon: Icon(Icons.person_outline),
                 title: Text("profile")
                ),
                ]
              )
            ,
          
          floatingActionButton: FloatingActionButton(onPressed: (){
            Navigator.push(context, MaterialPageRoute(builder: (context) => AddComplaint()));
          },
          backgroundColor: Colors.white,
          child: Icon(Icons.add,color: Colors.blue,size: 32,),
          ),
          appBar: AppBar(
            title: Row(
              children: <Widget>[
                Text(
                  "My Complaints",
                  style: TextStyle(
                      color: Colors.white,
                      fontSize: 20),
                )
              ],
              crossAxisAlignment: CrossAxisAlignment.center,
              mainAxisAlignment: MainAxisAlignment.center,
            ),
            bottom: TabBar(
              tabs: <Widget>[
                Tab(
                  text: "Active",
                ),
                Tab(
                  text: "History",
                )
              ],
            ),
          ),
          body: FutureBuilder(
            future: getData(),
            builder: (BuildContext context,AsyncSnapshot snap){
                  print(snap.data);
                return ListView.builder(itemCount: snap.data.length,
          itemBuilder: (BuildContext context,int index){
            return ComplaintCard(
              prob: snap.data[index]['prob'],
              complN:  snap.data[index]['compN'],
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
            },
          )

          
        ));
  }
}
