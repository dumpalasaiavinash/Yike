import 'dart:math' as math;
import 'package:path_drawing/path_drawing.dart';
import 'package:flutter/material.dart';

num degToRad(num deg) => deg * (math.pi / 180.0);

class CusBottomNavigationBar extends StatefulWidget {
  CusBottomNavigationBar({
    Key key,
    @required this.items,
    this.onTap,
    this.currentIndex = 0,
    this.elevation = 8.0,
    BottomNavigationBarType type,
    Color fixedColor,
    this.backgroundColor,
    this.selectedFontSize = 14.0,
    this.selectedLabelStyle,
    this.showSelectedLabels = true,
  })  : assert(items != null),
        assert(items.length >= 2),
        assert(0 <= currentIndex && currentIndex < items.length),
        assert(elevation != null && elevation >= 0.0),
        assert(selectedFontSize != null && selectedFontSize >= 0.0),
        assert(showSelectedLabels != null),
        super(key: key);

  final List<String> items;
  final ValueChanged<int> onTap;
  final int currentIndex;
  final double elevation;
  final Color backgroundColor;
  final TextStyle selectedLabelStyle;
  final double selectedFontSize;
  final bool showSelectedLabels;
  @override
  _BottomNavigationBarState createState() => _BottomNavigationBarState();
}

class _BottomTabs extends StatelessWidget {
  final String item;
  final VoidCallback onTap;
  final bool selected;
  final bool next;
  final bool prev;
  final double width;
  final double height;
  _BottomTabs(
    this.item,
    this.width,
    this.height, {
    this.selected = false,
    this.next = false,
    this.prev = false,
    this.onTap,
  });
  @override
  Widget build(BuildContext context) {
    Widget tab = selected
        ? (
          Stack(
                children: <Widget>[
          Container(
            margin: EdgeInsets.only(left: width / 3),
            width: width / 3,
            child: 
            CustomPaint(
              painter: ActiveTab(x0: width / 6, y0: 85),
              child: 
                  Padding(
                    padding: EdgeInsets.only(top: height / 6),
                    child: Text(
                      item,
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.white, fontSize: 24),
                    ),
                  ),
            ),),
            Container(
                    child: FlatButton(onPressed: onTap, child: Container(width: 40, height: 40,),),
                    width: 40,
                    height: 40,
                    margin:
                        EdgeInsets.only(left: (width * 1 / 2) - 20, top: 65),
                  ),
          ]))
        : next
            ? (
              Container(
                 
                width: width/3,
                margin:EdgeInsets.only(left: width*2/3),
                child: 
              CustomPaint(
                painter: NotActiveTab(x0: width * 1 / 6, y0: 115),
                child: Container(
                  child: FlatButton(onPressed: onTap, child: Container(width: 50, height: 50,),),
                  width: 40,
                  height: 40,
                  margin: EdgeInsets.only(left: (width *1/6) - 20, top: 95,right: (width*1/6)-20),
                ),
              )))
            : prev
                ? (CustomPaint(
                    painter: NotActiveTab(x0: width / 6, y0: 115),
                    child: Container(
                      child: FlatButton(onPressed:onTap, child: Container(width: 50, height: 50,),),
                      width: 50,
                      height: 50,
                      margin:
                          EdgeInsets.only(left: (width * 1 / 6) - 20, top: 95),
                    ),
                  ))
                : Container();

    return tab;
  }
}

class _BottomNavigationBarState extends State<CusBottomNavigationBar>
    with TickerProviderStateMixin {
  List<AnimationController> _controllers = <AnimationController>[];
  List<CurvedAnimation> _animations;

  Color _backgroundColor;

  static final Animatable<double> _flexTween =
      Tween<double>(begin: 1.0, end: 1.5);

  void _resetState() {
    print("Lol");
    _backgroundColor = widget.backgroundColor;
    for (AnimationController controller in _controllers) controller.dispose();
    _controllers =
        List<AnimationController>.generate(widget.items.length, (int index) {
      return AnimationController(
        duration: kThemeAnimationDuration,
        vsync: this,
      )..addListener(_rebuild);
    });
    _animations =
        List<CurvedAnimation>.generate(widget.items.length, (int index) {
      return CurvedAnimation(
        parent: _controllers[index],
        curve: Curves.fastOutSlowIn,
        reverseCurve: Curves.fastOutSlowIn.flipped,
      );
    });
    _controllers[widget.currentIndex].value = 0;
  }

  @override
  void initState() {
    super.initState();
    _resetState();
  }

  void _rebuild() {
    setState(() {
      // Rebuilding when any of the controllers tick, i.e. when the items are
      // animated.
    });
  }

  @override
  void dispose() {
    for (AnimationController controller in _controllers) controller.dispose();
    super.dispose();
  }

  double _evaluateFlex(Animation<double> animation) =>
      _flexTween.evaluate(animation);

  @override
  void didUpdateWidget(CusBottomNavigationBar oldWidget) {
    super.didUpdateWidget(oldWidget);
    // No animated segue if the length of the items list changes.
    if (widget.items.length != oldWidget.items.length) {
      _resetState();
      return;
    }

    if (widget.currentIndex != oldWidget.currentIndex) {
      _controllers[oldWidget.currentIndex].reverse();
      _controllers[widget.currentIndex].forward();
    }

  }

  // If the given [TextStyle] has a non-null `fontSize`, it should be used.
  // Otherwise, the [selectedFontSize] parameter should be used.
  static TextStyle _effectiveTextStyle(TextStyle textStyle, double fontSize) {
    textStyle ??= const TextStyle();
    // Prefer the font size on textStyle if present.
    return textStyle.fontSize == null
        ? textStyle.copyWith(fontSize: fontSize)
        : textStyle;
  }

  List<Widget> _createTabs(width, height) {
    List<Widget> tabs = [];

    for (int i = 0; i < widget.items.length; i++) {
      tabs.add(_BottomTabs(
        widget.items[i],
        width,
        height,
        onTap: () {
          if (widget.onTap != null) widget.onTap(i);
        },
        selected: i == widget.currentIndex,
        next: i - 1 == widget.currentIndex,
        prev: i + 1 == widget.currentIndex,
      ));
    }

    return tabs;
  }

  @override
  Widget build(BuildContext context) {
    assert(debugCheckHasDirectionality(context));
    assert(debugCheckHasMaterialLocalizations(context));
    assert(debugCheckHasMediaQuery(context));

    // Labels apply up to _bottomMargin padding. Remainder is media padding.
    final double additionalBottomPadding = math.max(
        MediaQuery.of(context).padding.bottom - widget.selectedFontSize / 2.0,
        0.0);
    final double width0 = MediaQuery.of(context).size.width;
    return Semantics(
      explicitChildNodes: true,
      child: Material(
        elevation: widget.elevation,
        child: Stack(
          children: <Widget>[
            Container(
              height: kBottomNavigationBarHeight * 3,
              width: width0,
              color: _backgroundColor,
            ),
            ConstrainedBox(
              constraints: BoxConstraints(
                  minHeight: kBottomNavigationBarHeight * 3, minWidth: width0),
              child: CustomPaint(
                painter: ArcLine(),
                child: Material(
                  // Splashes.
                  type: MaterialType.transparency,
                  child: Padding(
                    padding: EdgeInsets.only(bottom: additionalBottomPadding),
                    child: MediaQuery.removePadding(
                        context: context,
                        removeBottom: true,
                        child: _createTabsContainer(
                            width0,
                            kBottomNavigationBarHeight * 3,
                            _createTabs(
                                width0, kBottomNavigationBarHeight * 3))),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class ArcLine extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    Paint paint = Paint()
      ..color = Colors.white54
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;
    var startPoint = Offset(0, size.height);
    var controlPoint1 = Offset(size.width / 4, size.height / 3);
    var controlPoint2 = Offset(3 * size.width / 4, size.height / 3);
    var endPoint = Offset(size.width, size.height);

    var path = Path();
    path.moveTo(startPoint.dx, startPoint.dy);
    path.cubicTo(controlPoint1.dx, controlPoint1.dy, controlPoint2.dx,
        controlPoint2.dy, endPoint.dx, endPoint.dy);

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) {
    return true;
  }
}



class ActiveTab extends CustomPainter {
  final double x0, y0;
  ActiveTab({this.x0, this.y0});

  @override
  void paint(Canvas canvas, Size size) {
    Paint paint2 = Paint()
      ..color = Color.fromRGBO(0, 0, 0, 0.37)
      ..strokeWidth = 10
      ..style = PaintingStyle.fill;


    paint2 = Paint()
      ..color = Color.fromRGBO(212, 175, 55, 1)
      ..strokeWidth = 4
      ..style = PaintingStyle.fill;

    canvas.drawCircle(Offset(x0, y0), 7.5, paint2);

    paint2 = Paint()
      ..color = Color.fromRGBO(212, 175, 55, 1)
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    Path path = Path();
    path.addArc(Rect.fromLTWH(x0 - 12.5, y0 - 12.5, 25, 25), 0, 360);
    canvas.drawPath(
        dashPath(
          path,
          dashArray: CircularIntervalList<double>(<double>[1.0, 4.0]),
        ),
        paint2);

    paint2 = Paint()
      ..color = Colors.white24
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;
    path = Path();
    path.moveTo(x0 - 20, y0 - 20);
    path.addArc(
        Rect.fromLTWH(x0 - 20, y0 - 20, 10, 10), degToRad(180), degToRad(90));
    path.lineTo(x0 + 15, y0 - 20);
    path.addArc(
        Rect.fromLTWH(x0 + 10, y0 - 20, 10, 10), degToRad(270), degToRad(90));
    path.lineTo(x0 + 20, y0 + 15);
    path.addArc(
        Rect.fromLTWH(x0 + 10, y0 + 10, 10, 10), degToRad(360), degToRad(90));
    path.lineTo(x0 - 15, y0 + 20);
    path.addArc(
        Rect.fromLTWH(x0 - 20, y0 + 10, 10, 10), degToRad(90), degToRad(90));
    path.lineTo(x0 - 20, y0 - 15);
    canvas.drawPath(path, paint2);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => true;
}




class NotActiveTab extends CustomPainter {
  final double x0, y0;
  NotActiveTab({this.x0, this.y0});

  @override
  void paint(Canvas canvas, Size size) {
    Paint paint2;
      

    paint2 = Paint()
      ..color = Color.fromRGBO(212, 175, 55, 0.5)
      ..strokeWidth = 4
      ..style = PaintingStyle.fill;

    canvas.drawCircle(Offset(x0, y0), 6, paint2);

    Paint paint3 = Paint()
      ..color = Color.fromRGBO(212, 175, 55, 0.5)
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    Path path = Path();
    path.addArc(Rect.fromLTWH(x0 - 12, y0 - 12, 24, 24), 0, 360);
    canvas.drawPath(
        dashPath(
          path,
          dashArray: CircularIntervalList<double>(<double>[1.0, 4.0]),
        ),
        paint3);

    paint2 = Paint()
      ..color = Colors.white12
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    path = Path();
    path.moveTo(x0 - 20, y0 - 20);
    path.addArc(
        Rect.fromLTWH(x0 - 20, y0 - 20, 10, 10), degToRad(180), degToRad(90));
    path.lineTo(x0 + 15, y0 - 20);
    path.addArc(
        Rect.fromLTWH(x0 + 10, y0 - 20, 10, 10), degToRad(270), degToRad(90));
    path.lineTo(x0 + 20, y0 + 15);
    path.addArc(
        Rect.fromLTWH(x0 + 10, y0 + 10, 10, 10), degToRad(360), degToRad(90));
    path.lineTo(x0 - 15, y0 + 20);
    path.addArc(
        Rect.fromLTWH(x0 - 20, y0 + 10, 10, 10), degToRad(90), degToRad(90));
    path.lineTo(x0 - 20, y0 - 15);

    canvas.drawPath(path, paint2);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => true;
}

Widget _createTabsContainer(width, height, listWidgets) {
  return Container(
      width: width,
      height: height,
      child: Stack(
        children: listWidgets,
      ));
}
