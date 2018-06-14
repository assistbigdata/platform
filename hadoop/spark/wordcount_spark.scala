%spark
sc.textFile("s3://kr.assist.2018.emr/data/obama.txt")
    .flatMap(_.split("\\s+"))
    .map(_.toLowerCase.replaceAll("\\W",""))
    .filter(_.size >0)     
    .groupBy(identity)
    .map(x => x._2.size -> x._1)
    .sortByKey(false,1).foreach(println)
