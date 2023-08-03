// implement main.dart first for the db and init the daemon/proxy (user settings and stuff), then use db data to do stuff.

import "dart:io";
import "daemontools/db.dart";

class LentoDaemon{
  var taskDict = Map();
  var mainTimer = null;
  var task = null;
  var numAcceptors;

  LentoDaemon(numAcceptors){
    this.numAcceptors = numAcceptors;
  }

  void entry() {
    init(); // init the db

    var taskList = getAllTimerTasks();
  }
}
