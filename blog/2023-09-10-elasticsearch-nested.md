---
title: Elasticsearch Nested
tags: [database,elasticsearch]
---

> `nested` 结构允许在单个文档中嵌套子文档以优化结构，在某些业务中能发挥重要作用。
<!--truncate-->

### mapping
```js
{
  "person" : {
    "type" : "nested",
    "dynamic" : "strict",
    "properties" : {
      "name":{
        "type":"keyword"
      },
      "age":{
        "type":"integer"
      }
    }
  }
}
```


### query
```js
// dsl
{
  "query": {
    "nested":{
      "path": "person",
      "query":{
        "match": {
          "person.name": "person_name"
        }
      },
      "inner_hits": {"size":1}
    }
  }
}
```

返回
```js
{
    "hits" : [
      {
        "_index" : "test_index",
        "_type" : "_doc",
        "_id" : "test_id",
        "_score" : 15.236248,
        "_source" : {
          ...
        },
        "inner_hits" : {   //"inner_hits": {"size":1}
          "person" : {
            "hits" : {
              "total" : {
                "value" : 1,
                "relation" : "eq"
              },
              "max_score" : 15.236248,
              "hits" : [
                {
                  "_source" : {
                    "name":"a",
                    "age":18
                  }
                }
              ]
            }
          }
        }
      }]
  }
}
```

### sort
排序: inner_hits 排序只是doc内部的排序，所以需要在外层再次排序才能得到理想的结果
```js
"sort": {
    "person.age": {
        "order": "asc",
        "nested_path": "person",
        "nested_filter": {
            "match": {
                "person.name": "name"
            }
        }
    }
}
```

### agg
[click](https://blog.csdn.net/allenalex/article/details/45080645/)


