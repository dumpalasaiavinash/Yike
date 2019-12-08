import 'package:flutter/material.dart';
import 'package:yike_mobile_app/Pages/complaint_form_page.dart';
import 'package:yike_mobile_app/Widgets/complint_form.dart';

class AddComplaint extends StatelessWidget {
  List<OrgSearch> org = [
    OrgSearch(
        formId:"testform11",
        orgName: "PixaBay",
        orgLogo:
            "https://s3-ap-south-1.amazonaws.com/yike-s3/pixabay.png"),
    OrgSearch(
        formId:"testform12",
        orgName: "hello",
        orgLogo:
            "https://s3-ap-south-1.amazonaws.com/yike-s3/hello.png"),
    OrgSearch(
        formId:"testform13",
        orgName: "IOTA",
        orgLogo:
            "https://s3-ap-south-1.amazonaws.com/yike-s3/IOTA.jpg"),
    
  ];

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
                  "Register Complaint",
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 20,
                  ),
                  textAlign: TextAlign.center,
                ),
              ),
              Text(
                "Help",
                style: TextStyle(fontSize: 16, color: Colors.white),
              )
            ],
          ),
        ),
        body: Column(
          children: <Widget>[
            Container(
              color: Colors.indigo,
              margin: EdgeInsets.all(0),
              child: Container(
                color: Colors.indigo,
                margin: EdgeInsets.only(left: 16),
                child:TextFormField(
                decoration: InputDecoration(
                  hintText: "Search Orgnistaion here",
                  hintStyle: TextStyle(
                    color: Color.fromRGBO(255, 255, 255, 0.6),
                  ),
                  focusColor: Color.fromRGBO(255, 255, 255, 0.9),

                ),),
              ),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: org.length,
                itemBuilder: (BuildContext context, int index) {
                  return InkWell(
                      onLongPress: (){
                        print("HELLO");
                        Navigator.push(context, MaterialPageRoute(builder: (context) => Complaint_Form(formId: org[index].formId,)));},
                      onDoubleTap: (){
                        print("HELLO");
                        Navigator.push(context, MaterialPageRoute(builder: (context) => Complaint_Form(formId: org[index].formId,)));}, 
                      onTap: (){
                        print("HELLO");
                        Navigator.push(context, MaterialPageRoute(builder: (context) => Complaint_Form(formId: org[index].formId,)));},
                      child:Card(
                    margin:
                        EdgeInsets.only(bottom: 4, top: 4, right: 16, left: 16),
                    color: Colors.white,
                    elevation: 4,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                    child:
                     ListTile(
                      onTap: () {},
                      title: OrgTile(
                        orgLogo: org[index].orgLogo,
                        orgName: org[index].orgName,
                      ),
                    ),
                  ));
                },
              ),
            )
          ],
        ));
  }
}

class OrgTile extends StatelessWidget {
  final String orgLogo, orgName;
  OrgTile({this.orgLogo, this.orgName});
  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return Row(
      crossAxisAlignment: CrossAxisAlignment.center,
      mainAxisAlignment: MainAxisAlignment.start,
      children: <Widget>[
        Container(
          padding: EdgeInsets.fromLTRB(16, 16, 16, 16),
          child: CircleAvatar(
            backgroundColor: Colors.red,
            maxRadius: 15,
            minRadius: 10,
            child: Image.network(orgLogo),
          ),
        ),
        Container(
          child: Text(orgName,
              style: TextStyle(color: Colors.black87, fontSize: 16)),
        )
      ],
    );
  }
}

class OrgSearch {
  final String orgName;
  final String orgLogo;
  final String formId;
  OrgSearch({this.orgName, this.orgLogo, this.formId});
}
