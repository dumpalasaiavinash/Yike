import 'package:flutter/material.dart';

class ComplaintTimline extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    return _ComplaintTimlineState();
  }
}

class _ComplaintTimlineState extends State<ComplaintTimline> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
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
              child: Text(
                "Complaint Timeline",
                style: TextStyle(
                    fontSize: 20,
                    color: Colors.black87,
                    fontWeight: FontWeight.bold),
              ),
              padding:EdgeInsets.fromLTRB(8, 16, 16, 8),

            ),
            TimelineChild(
              color: Color.fromRGBO(123, 229, 187, 1),
              heading: "Complaint Recived",
              date: "28 Oct 2019",
            ),
            TimelineChild(
              color: Color.fromRGBO(123, 229, 187, 1),
              heading: "Complaint Forwarded to CCE",
              date: "28 Oct 2019",
            ),
            TimelineChild(
              color: Color.fromRGBO(123, 229, 187, 1),
              heading: "Complaint Recived by CCE",
              date: "28 Oct 2019",
            ),
            TimelineChild(
              color: Colors.black54,
              heading: "Yet to Assign to Agent",
              date: "28 Oct 2019",
            ),
            TimelineChild(
              color: Colors.black38,
              heading: "Estimated Completion",
              date: "7 Nov 2019",
              isLast: true,
            ),
            Container(margin:EdgeInsets.only(bottom: 16) ,),
          ],
          //
        ));
  }
}

class TimelineChild extends StatelessWidget {
  final Color color;
  final String heading, date;
  final bool isLast;
  TimelineChild({this.color, this.date, this.heading, this.isLast = false});

  @override
  Widget build(BuildContext context) {
    Widget widget = isLast
        ? Container(
            margin: EdgeInsets.fromLTRB(16, 12, 16, 0),
            child: Icon(Icons.fiber_manual_record, color: color, size: 14),
          )
        : Column(
            children: <Widget>[
              Container(
                margin: EdgeInsets.fromLTRB(16, 12, 16, 0),
                child: Icon(Icons.fiber_manual_record, color: color, size: 14),
              ),
              Container(
                margin: EdgeInsets.fromLTRB(16, 4, 16, 0),
                child: Icon(Icons.fiber_manual_record, color: color, size: 6),
              ),
              Container(
                margin: EdgeInsets.fromLTRB(16, 4, 16, 0),
                child: Icon(Icons.fiber_manual_record, color: color, size: 6),
              ),
              Container(
                margin: EdgeInsets.fromLTRB(16, 4, 16, 0),
                child: Icon(Icons.fiber_manual_record, color: color, size: 6),
              ),
              Container(
                margin: EdgeInsets.fromLTRB(16, 8, 16, 0),
                child: Icon(Icons.fiber_manual_record, color: color, size: 8),
              ),
            ],
          );

    // TODO: implement build
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        widget,
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisAlignment: MainAxisAlignment.start,
            children: <Widget>[
              Container(
                margin: EdgeInsets.fromLTRB(0, 8, 16, 4),
                child: Text(
                  heading,
                  style: TextStyle(
                      fontSize: 16,
                      color: Colors.black87,
                      fontWeight: FontWeight.bold),
                ),
              ),
              Text(
                date,
                style: TextStyle(fontSize: 14, color: Colors.black54),
              )
            ],
          ),
        )
      ],
    );
  }
}
