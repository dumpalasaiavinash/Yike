import 'package:flutter/material.dart';

class AddComplaint extends StatelessWidget {
  List<OrgSearch> org = [
    OrgSearch(
        orgName: "Amazon pvt. Ltd.",
        orgLogo:
            "https://www.clipartwiki.com/clipimg/detail/297-2971739_icon-amazon-logo-png.png"),
    OrgSearch(
        orgName: "Amazon pvt. Ltd.",
        orgLogo:
            "https://www.clipartwiki.com/clipimg/detail/297-2971739_icon-amazon-logo-png.png"),
    OrgSearch(
        orgName: "Amazon pvt. Ltd.",
        orgLogo:
            "https://www.clipartwiki.com/clipimg/detail/297-2971739_icon-amazon-logo-png.png"),
    OrgSearch(
        orgName: "Amazon pvt. Ltd.",
        orgLogo:
            "https://www.clipartwiki.com/clipimg/detail/297-2971739_icon-amazon-logo-png.png"),
    OrgSearch(
        orgName: "Amazon pvt. Ltd.",
        orgLogo:
            "https://www.clipartwiki.com/clipimg/detail/297-2971739_icon-amazon-logo-png.png"),
    OrgSearch(
        orgName: "Amazon pvt. Ltd.",
        orgLogo:
            "https://www.clipartwiki.com/clipimg/detail/297-2971739_icon-amazon-logo-png.png"),
    OrgSearch(
        orgName: "Amazon pvt. Ltd.",
        orgLogo:
            "https://www.clipartwiki.com/clipimg/detail/297-2971739_icon-amazon-logo-png.png"),
  ];

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
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
              color: Colors.blue,
              margin: EdgeInsets.all(0),
              child: TextFormField(
                decoration: InputDecoration(
                  hintText: "Search Orgnistaion here",
                  hintStyle: TextStyle(
                    color: Color.fromRGBO(255, 255, 255, 0.6),
                  ),
                  focusColor: Color.fromRGBO(255, 255, 255, 0.9),

                ),
              ),
            ),
            Expanded(
              child: ListView.builder(
                itemCount: org.length,
                itemBuilder: (BuildContext context, int index) {
                  return Card(
                    margin:
                        EdgeInsets.only(bottom: 4, top: 4, right: 16, left: 16),
                    color: Colors.white,
                    elevation: 4,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                    child: ListTile(
                      onTap: () {},
                      title: OrgTile(
                        orgLogo: org[index].orgLogo,
                        orgName: org[index].orgName,
                      ),
                    ),
                  );
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
  OrgSearch({this.orgName, this.orgLogo});
}
