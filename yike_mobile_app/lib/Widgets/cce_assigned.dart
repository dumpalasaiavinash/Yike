import 'package:flutter/material.dart';

class AssignedCCE extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Card(
      margin: EdgeInsets.only(bottom: 8, top: 8, right: 16, left: 16),
      color: Colors.white,
      elevation: 10,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(10.0),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: <Widget>[
          Container(
            child: Text("Assigned CCE",
            style: TextStyle(
                    fontSize: 20,
                    color: Colors.black87,
                    fontWeight: FontWeight.bold),),
            margin: EdgeInsets.only(top: 16, bottom:4, left: 16),
          ),
          Row(
            children: <Widget>[
              Container(
                child: CircleAvatar(
                  maxRadius: 30,
                  minRadius: 20,
                  backgroundColor: Colors.orange,
                ),
                padding: EdgeInsets.all(8),
              ),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Text(
                      "Sai Pranay Raju",
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.black87,
                        fontSize: 18,
                      ),
                    ),
                    Text(
                      "Junior Technical Assitant",
                      style: TextStyle(color: Colors.black54, fontSize: 14),
                    )
                  ],
                ),
              )
            ],
            crossAxisAlignment: CrossAxisAlignment.center,
          )
        ],
      ),
    );
  }
}
