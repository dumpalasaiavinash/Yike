import 'dart:async';
import 'package:flutter/material.dart';
import 'package:yike_mobile_app/Pages/complaint_detail.dart';

class ComplaintCard extends StatefulWidget {
  final bool haveprob;
  final String org_name, compl, comp_date, status, prob, date, time, complN;
  ComplaintCard(
      {this.haveprob = false,
      this.org_name,
      this.compl,
      this.comp_date,
      this.status,
      this.prob = "",
      this.date,
      this.time,
      this.complN});
  @override
  State<StatefulWidget> createState() {
    // TODO: implement createState
    return _ComplaintCardState();
  }
}

class _ComplaintCardState extends State<ComplaintCard> {
  Size cardSize = Size(10, 0);
  double wi = 10;
  EdgeInsetsGeometry _margin, _padding;
  bool _haveprob = false;
  Color _color = Colors.green;
  String _org_name,
      _compl,
      _comp_date,
      _status,
      _prob,
      _date,
      _time,
      _complN,
      _line2;
  Timer _timer;
  Widget _probWidget;
  GlobalKey _keyCard = GlobalKey(), _keyProb = GlobalKey();
  Size _getSizes() {
    final RenderBox renderBox = _keyCard.currentContext.findRenderObject();
    final sizeCard = renderBox.size;
    return sizeCard;
  }

  @override
  void initState() {
    // TODO: implement initState

    _org_name = widget.org_name;
    _prob = widget.prob;
    _haveprob = widget.haveprob;
    _color = _haveprob ? Colors.orange : Colors.green;
    _compl = widget.compl;
    _complN = widget.complN;
    _status = widget.status;
    _date = widget.date;
    _comp_date = widget.comp_date;
    _time = widget.time;
    _margin =
        _haveprob ? EdgeInsets.fromLTRB(16, 12, 16, 4) : EdgeInsets.all(0);
    _padding =
        _haveprob ? EdgeInsets.fromLTRB(16, 12, 16, 4) : EdgeInsets.all(0);
    // print(_date);

    _line2 =
        "#" + _complN + "\t\t\t \u23f0 " + _date + " \t\t\t\u23f0 " + _time;
    _probWidget = _haveprob
        ? (Row(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: <Widget>[
              Icon(Icons.error_outline),
              Container(
                width: 250,
                // width: MediaQuery.of(context).size.width*0.7,
                child: Text(_prob),
              ),
            ],
          ))
        : Container();
    super.initState();
    _timer = new Timer(const Duration(milliseconds: 400), () {
      setState(() {
        cardSize = _getSizes();
        wi = _haveprob ? _getSizes().width * 0.8 : 0;
        print(wi);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    // TODO: implement build
    return new GestureDetector(
      onTap: () {Navigator.push(context,  MaterialPageRoute(builder: (context) => ComplaintDetails()));},
      child: Card(
        key: _keyCard,
        margin: EdgeInsets.only(bottom: 8, top: 8, right: 16, left: 16),
        color: Colors.white,
        elevation: 10,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10.0),
        ),
        child: Wrap(
          children: <Widget>[
            Row(
              children: <Widget>[
                Container(
                  width: 10,
                  height: cardSize.height,
                  decoration: BoxDecoration(
                      color: _color,
                      borderRadius: BorderRadius.only(
                          topLeft: Radius.circular(10),
                          bottomLeft: Radius.circular(10))),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: <Widget>[
                    Row(
                      children: <Widget>[
                        Container(
                          margin: EdgeInsets.fromLTRB(16, 16, 16, 8),
                          child: Image.asset(
                            "assets/yikelogo.png",
                            width: 30,
                            height: 30,
                          ),
                        ),
                        Text(
                          _org_name,
                          style: TextStyle(
                              color: Colors.black87,
                              fontSize: 18,
                              fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    Container(
                      margin: EdgeInsets.fromLTRB(16, 0, 16, 0),
                      width: MediaQuery.of(context).size.width * 0.8,
                      child: Text(
                        _compl,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                            color: Colors.black87,
                            fontSize: 16,
                            fontWeight: FontWeight.bold),
                      ),
                    ),
                    Container(
                      margin: EdgeInsets.fromLTRB(16, 8, 16, 16),
                      child: Text(
                        _line2,
                        //
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                          color: Colors.black45,
                          fontSize: 12,
                        ),
                      ),
                    ),
                    Container(
                      margin: EdgeInsets.fromLTRB(16, 0, 16, 4),
                      child: Row(
                        children: <Widget>[
                          Text(
                            "Estimated Completion:",
                            style: TextStyle(
                                color: Colors.black87,
                                fontSize: 14,
                                fontWeight: FontWeight.bold),
                          ),
                          Text(
                            _comp_date,
                            style: TextStyle(
                              color: Colors.black45,
                              fontSize: 13,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      margin: EdgeInsets.fromLTRB(16, 0, 16, 4),
                      child: Row(
                        children: <Widget>[
                          Text(
                            "Status:",
                            style: TextStyle(
                                color: Colors.black87,
                                fontSize: 14,
                                fontWeight: FontWeight.bold),
                          ),
                          Text(
                            _status,
                            style: TextStyle(
                              color: Colors.black45,
                              fontSize: 13,
                            ),
                          ),
                        ],
                      ),
                    ),
                    Container(
                      margin: _margin,
                      padding: _padding,
                      decoration: BoxDecoration(
                        color: Colors.orange[200],
                        borderRadius: BorderRadius.circular(5.0),
                      ),
                      width: wi,
                      child: _probWidget,
                    )
                    /**/
                  ],
                )
              ],
            ),
          ],
        ),
      ),
    );
  }
}
