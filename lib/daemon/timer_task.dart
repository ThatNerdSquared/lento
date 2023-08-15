
class TimerTask{
  String test = '';
  String name = '';
  int taskInterval = 0;
  dynamic appBlocker; // change type later
  dynamic proxy; // chnage type later
  Map appBlockItems = {};
  Map websiteBlockItems = {};

  TimerTask(Map cardInfo){
    // placeholder
  }

  TimerTask.init(this.name, this.taskInterval, this.appBlocker, this.proxy, this.appBlockItems, this.websiteBlockItems);


  void start(TimerTask task){
    // placeholder
  }

  void printBlockData() {
    // placeholder
  }

  void startTimer(int time) {
    // placeholder
  }

  Map appBlockItemConverter (Map cardInfo) {
    // placeholder
    return cardInfo;
  }

  Map siteBlockItemConverter (Map cardInfo) {
    // placeholder
    return cardInfo;
  }


  void cleanup(){
    // placeholder
  }

}