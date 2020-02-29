/*
 Navicat Premium Data Transfer

 Source Server         : mongo
 Source Server Type    : MongoDB
 Source Server Version : 40009
 Source Host           : localhost:27017
 Source Schema         : facebook_lite

 Target Server Type    : MongoDB
 Target Server Version : 40009
 File Encoding         : 65001

 Date: 07/10/2019 12:10:00
*/


// ----------------------------
// Collection structure for comment
// ----------------------------
db.getCollection("comment").drop();
db.createCollection("comment");

// ----------------------------
// Documents of comment
// ----------------------------
session = db.getMongo().startSession();
session.startTransaction();
db = session.getDatabase("facebook_lite");
db.getCollection("comment").insert([ {
    _id: ObjectId("5d999cdff981e47d181d3a32"),
    post: "5d997f5f7dba9969cc448e12",
    user: "admi12121n2121",
    content: "1w121",
    datetime: "2019-10-06 07:50:55am"
} ]);
db.getCollection("comment").insert([ {
    _id: ObjectId("5d999de77ad2fd447677b0a2"),
    post: "5d997f68ac06066dea0aef13",
    user: "admi12121n2121",
    content: "asas",
    datetime: "2019-10-06 07:55:19am"
} ]);
db.getCollection("comment").insert([ {
    _id: ObjectId("5d999e2898096a09bd55f977"),
    post: "5d998d1dbc6a6442952f1293",
    user: "admi12121n2121",
    content: "hhh",
    datetime: "2019-10-06 07:56:24am"
} ]);
db.getCollection("comment").insert([ {
    _id: ObjectId("5d999ee95912e82dbb6c0944"),
    post: null,
    user: "admi12121n2121",
    content: "iView 使用较为安全的蓝色作为主色调，其中 Light Primary 常用于 hover，Dark Primary 常用于 active。",
    datetime: "2019-10-06 07:59:37am"
} ]);
db.getCollection("comment").insert([ {
    _id: ObjectId("5d999ef3d8103734ab1b53d2"),
    post: "5d999ee95912e82dbb6c0946",
    user: "admi12121n2121",
    content: "$a=array(0=>array(\"name\"=>\"a\",\"mail\"=>\"b\"),1=>array(\"name\"=>\"d\",\"mail\"=>\"e\"),2=>array('name'=>'aaa','mail'=>'hhehe'));\r\n\r\nfunction addkey(&$val, $key, $param)\r\n{\r\n    $val[$param['key']] = $param['val'];\r\n}\r\n\r\narray_walk($a,'addkey',array('key'=>'tel', 'val'=>'123'));\r\nprint_r($a);",
    datetime: "2019-10-06 07:59:47am"
} ]);
db.getCollection("comment").insert([ {
    _id: ObjectId("5d99ab187ad2fd447677b0a4"),
    post: "5d997f68ac06066dea0aef13",
    user: "jack",
    content: "asdas",
    datetime: "2019-10-06 08:51:36am"
} ]);
db.getCollection("comment").insert([ {
    _id: ObjectId("5d99afcc98096a09bd55f978"),
    post: null,
    user: "大大大大大",
    content: "hillosassdas",
    datetime: "2019-10-06 09:11:40am"
} ]);
db.getCollection("comment").insert([ {
    _id: ObjectId("5d99afd298096a09bd55f97c"),
    post: "5d99afcc98096a09bd55f97a",
    user: "大大大大大",
    content: "sasasa",
    datetime: "2019-10-06 09:11:46am"
} ]);
session.commitTransaction(); session.endSession();

// ----------------------------
// Collection structure for friendship
// ----------------------------
db.getCollection("friendship").drop();
db.createCollection("friendship");

// ----------------------------
// Documents of friendship
// ----------------------------
session = db.getMongo().startSession();
session.startTransaction();
db = session.getDatabase("facebook_lite");
db.getCollection("friendship").insert([ {
    _id: ObjectId("5d99a9339f91022b2e694914"),
    own: "1140182402@qq.com",
    friend: "admin"
} ]);
db.getCollection("friendship").insert([ {
    _id: ObjectId("5d99ae3c3e20880245539872"),
    own: "admin",
    friend: "1140182402@qq.com"
} ]);
db.getCollection("friendship").insert([ {
    _id: ObjectId("5d99afde7ad2fd447677b0a6"),
    own: "1140182402@qq.com",
    friend: "1@1.com"
} ]);
db.getCollection("friendship").insert([ {
    _id: ObjectId("5d99afe5c8706473ac4429c2"),
    own: "1@1.com",
    friend: "1140182402@qq.com"
} ]);
session.commitTransaction(); session.endSession();

// ----------------------------
// Collection structure for post
// ----------------------------
db.getCollection("post").drop();
db.createCollection("post");

// ----------------------------
// Documents of post
// ----------------------------
session = db.getMongo().startSession();
session.startTransaction();
db = session.getDatabase("facebook_lite");
db.getCollection("post").insert([ {
    _id: ObjectId("5d997f5f7dba9969cc448e12"),
    user: "admin",
    content: "sadsdfs",
    datetime: "2019-10-06 05:45:03am"
} ]);
db.getCollection("post").insert([ {
    _id: ObjectId("5d997f68ac06066dea0aef13"),
    user: "admin",
    content: "dsfdsfdfdsd",
    datetime: "2019-10-06 05:45:12am"
} ]);
db.getCollection("post").insert([ {
    _id: ObjectId("5d99afcc98096a09bd55f97a"),
    user: "1@1.com",
    content: "hillosassdas",
    datetime: "2019-10-06 09:11:40am"
} ]);
session.commitTransaction(); session.endSession();

// ----------------------------
// Collection structure for user
// ----------------------------
db.getCollection("user").drop();
db.createCollection("user");

// ----------------------------
// Documents of user
// ----------------------------
session = db.getMongo().startSession();
session.startTransaction();
db = session.getDatabase("facebook_lite");
db.getCollection("user").insert([ {
    _id: ObjectId("5d99a91cd8103734ab1b53d3"),
    email: "1140182402@qq.com",
    password: "1234",
    "full_name": "jack",
    "screen_name": "jack",
    birth: "1999-02-04",
    location: "kkk",
    gender: "female",
    status: "online",
    visibility: "everyone"
} ]);
db.getCollection("user").insert([ {
    _id: ObjectId("5d99afb1d8103734ab1b53d4"),
    email: "1@1.com",
    password: "1234",
    "full_name": "first",
    "screen_name": "大大大大大",
    birth: "2019-10-04",
    location: "1121",
    gender: "female",
    status: "busy",
    visibility: "private"
} ]);
session.commitTransaction(); session.endSession();

// ----------------------------
// Collection structure for userlike
// ----------------------------
db.getCollection("userlike").drop();
db.createCollection("userlike");

// ----------------------------
// Documents of userlike
// ----------------------------
session = db.getMongo().startSession();
session.startTransaction();
db = session.getDatabase("facebook_lite");
db.getCollection("userlike").insert([ {
    _id: ObjectId("5d999e2398096a09bd55f976"),
    user: "admin",
    post: "5d997f5f7dba9969cc448e12"
} ]);
db.getCollection("userlike").insert([ {
    _id: ObjectId("5d999ee95912e82dbb6c0945"),
    user: "admin",
    post: null
} ]);
db.getCollection("userlike").insert([ {
    _id: ObjectId("5d99afcc98096a09bd55f979"),
    user: "1@1.com",
    post: null
} ]);
session.commitTransaction(); session.endSession();
