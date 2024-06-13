import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';
import recentPost from './recentPost';
import { Button } from 'antd';


function Feature({url, title, desc}) {
  return (
    <div style={{width:"100%",marginBottom:20}}>
      <Link to={url}><h3>{title}</h3></Link>
      <p>{ desc}</p>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <div>
      <section className={styles.features}>
        <div className="container" style={{paddingLeft:12}}>
          <span style={{ fontWeight: 600 }}>分类</span>:&nbsp;&nbsp;{recentPost.tags.map((props, idx) => (
            <Button style={{ padding: 5, marginRight: 10, borderRadius: 5 ,color:"green"}} type="link"><Link to={`/blog/tags/${props[0]}`}>{props[0]}({props[1]})</Link></Button>
          ))
          }
        </div>
      </section>
    <section className={styles.features}>
      <div className="container">
        <div>
          {recentPost.blogs.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
        <Link to="/blog" >查看所有文章</Link>
        </div>
        
      </section>
      
    </div>
  );
}
