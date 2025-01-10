declare namespace JSX {
    interface IntrinsicElements {
      'langflow-chat': {
        window_title?: string;
        flow_id?: string;
        host_url?: string;
        [key: string]: any;
      }
    }
}