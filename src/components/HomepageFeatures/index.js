import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';
import Link from '@docusaurus/Link';
import recentPost from './recentPost';


function Feature({url, title, desc}) {
  return (
    <div style={{width:"100%",marginBottom:40}}>
      <Link to={url}><h2>{title}</h2></Link>
      <p>{ desc}</p>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <div>
      <section className={styles.features}>
        <div className="container" style={{paddingLeft:12}}>
          <span class="" style={{ fontWeight: 600 }}>分类</span>:&nbsp;&nbsp;{recentPost.tags.map((props, idx) => (
            <Link to={`/blog/tags/${props[0]}`} className={styles.tag}>{props[0]}<strong style={{ marginLeft: 5}}>{props[1]}</strong></Link>
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
