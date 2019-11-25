import 'package:flutter/material.dart';

class ComplaintForm extends StatefulWidget {
  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    return _ComplaintFormState();
  }
}

class _ComplaintFormState extends State<ComplaintForm> {
  List fields = [
    ['Orgnisation', 'textfield', ''],
    ['Complaint', 'textarea', 100],
    ['EMIE1 No', 'textfield', 16],
    ['EMIE1 No', 'textfield', 16],
    ['Bill SnapShot', 'image']
  ];
  List values = [
    'Redgear Pvt. Ltd.',
    'I bought Redgear Zonik wireless controller last aug from Amazon and it\'s RB button is not working as it is still in warranty period so i want to exchange it new one',
    '1234567894567',
    '9874561238574',
    'https://www.marshfieldclinic.org/Style%20Library/Images/billpay/LMC-Bill-2018.jpg',
  ];
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
  }

  List<Widget> _getWidgets() {
    List<Widget> form = [];
    form.add(
      Container(
        child: Text(
          "Complaint Details",
          style: TextStyle(
              fontSize: 20, color: Colors.black87, fontWeight: FontWeight.bold),
        ),
        padding: EdgeInsets.fromLTRB(8, 16, 16, 8),
      ),
    );
    for (int index = 0; index < fields.length; ++index) {
      String wt = fields[index][1];
      String label = fields[index][0];
      String val = values[index];
      //fields[index][2];
      if (wt == 'textfield') {
        print(values[index]);
        form.add(
          Container(
            padding: EdgeInsets.fromLTRB(16, 16, 16, 0),
            child: TextFormField(
              enabled: false,
              initialValue: val,
              decoration: InputDecoration(
                labelText: label,
                labelStyle: TextStyle(color: Colors.black87),
                focusedBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.blueAccent, width: 2.0),
                ),
                enabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.black38, width: 1.0),
                ),
                disabledBorder: OutlineInputBorder(
                  borderSide: BorderSide(color: Colors.black54, width: 1.0),
                ),
              ),
              style: TextStyle(color: Colors.black54),
            ),
          ),
        );
      } else if (wt == 'textarea') {
        form.add(Container(
          padding: EdgeInsets.fromLTRB(16, 16, 16, 0),
          child: TextFormField(
            maxLines: null,
            enabled: false,
            initialValue: val,
            decoration: InputDecoration(
              labelText: label,
              labelStyle: TextStyle(color: Colors.black87),
              focusedBorder: OutlineInputBorder(
                borderSide: BorderSide(color: Colors.blueAccent, width: 2.0),
              ),
              enabledBorder: OutlineInputBorder(
                borderSide: BorderSide(color: Colors.black38, width: 1.0),
              ),
              disabledBorder: OutlineInputBorder(
                borderSide: BorderSide(color: Colors.black54, width: 1.0),
              ),
            ),
            style: TextStyle(color: Colors.black54),
          ),
        ));
      } else if (wt == 'image') {
        form.add(Container(
          child: Column(
            children: <Widget>[
              Container(
                child: Text(label),
                padding: EdgeInsets.fromLTRB(16, 16, 16, 0),
              ),
              Container(
                padding: EdgeInsets.fromLTRB(16,16,16,50),
                child: Image.network(
                val,
                width: MediaQuery.of(context).size.width * 0.8,
              ),)
              
            ],
            crossAxisAlignment: CrossAxisAlignment.start,
          ),
        ));
      } else {
        form.add(Text("not supported yet"));
      }
    }
    return form;
  }

  @override
  Widget build(BuildContext context) {
    List<Widget> widgets = _getWidgets();

    return  Card(
        margin: EdgeInsets.only(bottom: 8, top: 8, right: 16, left: 16),
        color: Colors.white,
        elevation: 10,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10.0),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: widgets,
        ));
  }
}