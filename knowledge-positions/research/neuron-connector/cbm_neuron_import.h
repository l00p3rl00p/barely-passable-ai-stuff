/* Include in CBM src/main.c; uses its native SQLite store and FTS functions.
 * Offline isolated existing project only. No rescan, no source execution.
 * Input is one bounded JSON object on stdin. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "store/store.h"
#include <yyjson/yyjson.h>

static const char *neuron_str(yyjson_val *o,const char *k) {
    return yyjson_get_str(yyjson_obj_get(o,k));
}
static int neuron_import(const char *path,const char *project,const char *root) {
    (void)root;
    int rc=1, begun=0;
    const size_t cap=8*1024*1024;
    char *buf=malloc(cap+1); if(!buf) return 1;
    size_t len=fread(buf,1,cap+1,stdin);
    if(len>cap || ferror(stdin)){free(buf);return 1;}
    yyjson_doc *doc=yyjson_read(buf,len,0); free(buf);
    if(!doc)return 1;
    yyjson_val *obj=yyjson_doc_get_root(doc),*nodes=yyjson_obj_get(obj,"nodes"),*edges=yyjson_obj_get(obj,"edges");
    cbm_store_t *s=NULL;
    if(!yyjson_is_arr(nodes)||!yyjson_is_arr(edges))goto done;
    s=cbm_store_open_path_existing(path); if(!s)goto done;
    if(cbm_store_begin(s)!=CBM_STORE_OK)goto done;
    begun=1;
    /* Existing project is a prerequisite; never register a new root or replace it. */
    size_t i,max; yyjson_val *v;
    yyjson_arr_foreach(nodes,i,max,v) {
        const char *label=neuron_str(v,"label"),*name=neuron_str(v,"name"),*qn=neuron_str(v,"qualified_name"),*file=neuron_str(v,"file_path"),*props=neuron_str(v,"properties");
        if(!label||!name||!qn||!file||!props)goto done;
        cbm_node_t existing={0};
        int found=cbm_store_find_node_by_qn(s,project,qn,&existing);
        /* Append only: no overwriting the native index or reviewed knowledge. */
        if(found!=CBM_STORE_NOT_FOUND)goto done;
        cbm_node_t node={.project=project,.label=label,.name=name,.qualified_name=qn,.file_path=file,.start_line=yyjson_get_int(yyjson_obj_get(v,"start_line")),.end_line=yyjson_get_int(yyjson_obj_get(v,"end_line")),.properties_json=props};
        if(cbm_store_upsert_node(s,&node)<=0)goto done;
    }
    yyjson_arr_foreach(edges,i,max,v) {
        const char *a=neuron_str(v,"src"),*b=neuron_str(v,"dst"),*t=neuron_str(v,"type"),*props=neuron_str(v,"properties");
        if(!a||!b||!t||!props)goto done;
        cbm_node_t src={0},dst={0};
        if(cbm_store_find_node_by_qn(s,project,a,&src)!=CBM_STORE_OK ||
           cbm_store_find_node_by_qn(s,project,b,&dst)!=CBM_STORE_OK)goto done;
        cbm_edge_t edge={.project=project,.source_id=src.id,.target_id=dst.id,.type=t,.properties_json=props};
        if(cbm_store_insert_edge(s,&edge)<=0)goto done;
    }
    if(cbm_store_fts_rebuild(s,NULL,0)!=CBM_STORE_OK)goto done;
    if(cbm_store_commit(s)!=CBM_STORE_OK)goto done;
    begun=0; rc=0;
done:
    if(s){if(begun)cbm_store_rollback(s);cbm_store_close(s);}
    yyjson_doc_free(doc);
    if(!rc)puts("{\"ok\":true}");
    else fputs("CBM native emission refused; inspect existing project and schema\n",stderr);
    return rc;
}
